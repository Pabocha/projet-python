from django.shortcuts import render, redirect
from immobilier import settings
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from .forms import UserCreationForms, UserChangeForms
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# pour verifier les droits des utilisateurs
from django.contrib.admin.views.decorators import user_passes_test


# Pour l'envoie du mail
from django.core.mail import send_mail, EmailMessage
from decimal import Decimal
from investisseurs.models import Investisseur
from .models import Notification

# pour récuperer l'adresse du site
from django.contrib.sites.shortcuts import get_current_site

# pour generer un tokenunique à l'utilisateur
from immobilier.token import generatorToken
# Create your views here.

User = get_user_model()


def register(request):
    form = UserCreationForms()

    if request.method == 'POST':
        # récupération des données du formulaire
        form = UserCreationForms(data=request.POST)
        # verification du formulaire
        if form.is_valid(raise_exceptions=True):
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # recupération des données sauvegarder pour les utilisés
            firstname = form.cleaned_data['first_name']
            lastname = form.cleaned_data['last_name']
            email_user = form.cleaned_data['email']
            messages.success(
                request, f'votre comtpe à été créer avec success {firstname}.\n\n Nous vous avons envoyé un mail pour activer votre compte')

            # Envoie mail de bienvenue

            subject = "Bienvenue sur la plateforme Coopérative Contruisons ensemble"
            message = ("Bienvenue " + firstname + " " + lastname +
                       "\n Nous sommes ravi de vous comptez parmi nous \n\n\ Merci de votre envie de contruire avec nous \n\n Pablo Genius")
            from_email = settings.EMAIL_HOST_USER
            to_list = [email_user]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=False)

            subject = "Un utilisateur à été créer"
            message = ("Bonjour un utilisateur viens de s'incrire dans la plateforme Coopérative Construisons ensemble \n\n son Nom: " +
                       firstname + " " + lastname +
                       "\n\n Mercie de bien vouloir vérifié dans la base de données")

            from_email = settings.EMAIL_HOST_USER
            to_list = [from_email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=False)

            # Envoie mail d'activation

            current_site = get_current_site(request)
            email_subject = "Activation de votre compte"
            message_active = render_to_string("user_auth/email.html", {
                'name': firstname + " " + lastname,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generatorToken.make_token(user)
            })
            email = EmailMessage(
                email_subject,
                message_active,
                settings.EMAIL_HOST_USER,
                [email_user]
            )
            email.fail_silently = False
            email.send()
            return redirect('login')

    return render(request, 'user_auth/register.html', {'form': form})


# Fonction d'activation de compte
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Verification si user existe et que le token à bien été reçu et cliquer
    if user is not None and generatorToken.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, 'votre compte à bien été activé vous pouvez vous connectez')
        return redirect('login')
    else:
        messages.error(request, "votre compte n'a pas put être activé")
        return redirect('about')


def logine(request):
    # form = UserLogin()
    if request.method == 'POST':
        # récupération des données du formulaire
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username,
                            password=password)

        # Verifier si l'utilisateur existe
        try:
            my_user = User.objects.get(username=username)
        except:
            my_user = None

        if user is not None:
            login(request, user)

            # Sa c'est dans le cas où l'utilsateur cherche à rentrer dans une page où l'authentification est obligé
            # le site lui rédiregira vers la page de connexion
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)

            # La c'est si l'utilisateur se connecte directement dans la page de connexion
            else:
                return redirect('/')

        # Verification pour savoir si l'utilisateur à bien activé son compte grâce au mail d'activation envoyé
        elif my_user and my_user.is_active == False:
            messages.error(
                request, "votre compte n'est pas activé vérifier d'abord votre mail d'activation ")
        else:
            messages.error(
                request, "votre matricule ou votre mot de passe est incorrect ")
    return render(request, 'user_auth/login.html')


@login_required
@user_passes_test(lambda u: u.investisseur)
def compte(request):
    investisseur = Investisseur.objects.get(matricule=request.user.username)
    if investisseur.date_inscris is not None:
        mois_ecoule = relativedelta(timezone.now().date(), investisseur.date_inscris.date()).months
    else:
        mois_ecoule = "Aucun"
    context = {'investisseur': investisseur, 'mois_ecoule': mois_ecoule}
    if request.method == "POST":
        montant_retrait = request.POST['montant']

        # on verifie si le montant saisie n'est pas vide
        if montant_retrait != "":
            montant_retrait = Decimal(montant_retrait)
            if montant_retrait < 10000:
                messages.warning(request, "vous ne pouvez pas faire un retrait infèrieur à 10000 FCFA")
            elif investisseur.solde >= montant_retrait:
                if investisseur.retrait_en_attente == 0:
                    investisseur.solde -= montant_retrait
                    investisseur.retrait_en_attente = montant_retrait
                    investisseur.status_retrait = 'attente'
                    investisseur.save()
                    messages.success(
                        request, "votre retrait à été effectué avec success")
                    Notification.objects.create(matricule=request.user.username, nom=request.user.last_name, prenom=request.user.first_name, email=request.user.email,
                                                message="Une demande de retrait a été effectuer", type_message="retrait")
                else:
                    messages.error(
                        request, "vous avez déjà un retrait en attente")
            else:
                messages.error(request, "votre solde eest insuffisant")
        else:
            messages.error(request, "vous n'avez pas saisie un montant")
    return render(request, 'user_auth/compte.html', context)


def user_profile(request):
    user = User.objects.get(username=request.user.username)
    form = UserChangeForms(instance=user)
    if request.method == 'POST':
        form = UserChangeForms(request.POST, instance=user)
        if form.is_valid():
            form.save()
            investisseur = Investisseur.objects.filter(
                matricule=request.user.username)
            if investisseur.exists():
                prenom = form.cleaned_data.get('first_name')
                nom = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email')
                phone = form.cleaned_data.get('phone')
                investisseur.update(prenom=prenom, nom=nom,
                                    email=email, phone=phone)
                return redirect('compte')
    context = {'form': form}
    return render(request, 'user_auth/users-profile.html', context)


@login_required
def logoute(request):
    logout(request)
    return redirect('home')
