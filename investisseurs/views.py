from django.shortcuts import render, HttpResponse, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from immobilier import settings
from django.core.mail import send_mail, EmailMessage
from .models import Investissement, Investisseur
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from utilisateurs.models import Notification

user = get_user_model()
# Create your views here.


@login_required(login_url='login')
def investissement(request):
    if not request.user.membre:
        return render(request, "base/acces_refuse.html")
    investissement = Investissement.objects.all()
    context = {'investi': investissement}
    if request.method == 'POST':
        id_niveau = request.POST['investi_id']
        montant_investi = request.POST['montant']

        # permet de verifier si l'utilisateur n'a rien saisie
        if montant_investi != "":
            # on transforme le montant qu'il a saisit qui est en int en le transforme en decimal
            montant_investi = Decimal(montant_investi)
            niveau = Investissement.objects.get(id=id_niveau)
            matricule = request.user.username
            firstname = request.user.first_name
            lastname = request.user.last_name
            email = request.user.email
            phone = request.user.phone
            solde = 0

            # on initialise on ne le crée pas encore, on verifie d'abord les contraintes
            investisseur = Investisseur(matricule=matricule, prenom=firstname,
                                        nom=lastname, email=email, phone=phone, solde=solde, niveau=niveau, montant_investi=montant_investi)
            if montant_investi < niveau.montant_min:
                messages.error(request,
                               "le montant que vous avez saisie est infèrieur au niveau que vous avez choisi")
            elif montant_investi > niveau.montant_max:
                messages.error(
                    request, 'le montant que vous avez saisie est superieur au niveau que vous avez choisi veuillez choisir un niveau superieur')
            else:
                if not Investisseur.objects.filter(matricule=matricule).exists():

                    investisseur.save()
                    messages.success(
                        request, "votre investissement a été efectué avec success veuillez consulter votre boite mail pour finaliser l'investissement")
                    Notification.objects.create(matricule=matricule, nom=lastname, prenom=firstname, email=email,
                                                message="Un Utilisateur vient d'investir sur la plateforme", type_message="investissement")

                    # Envoie mail de pour finaliser l'investissement
                    subject = "Bienvenue sur la plateforme Coopérative Contruisons ensemble"
                    message = ("Bienvenue " + firstname + " " + lastname +
                               "\n Nous sommes ravi vous ayez investis sur notre plateforme votre compte a été crée et veuillez finaliser votre investissement en envoyant le montant de votre invstissement sur ce numéro 78 129 39 04 \n\n Merci de votre envie de contruire avec nous \n\n Pablo Genius")
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [email]
                    send_mail(subject, message, from_email,
                              to_list, fail_silently=False)
                else:
                    messages.error(
                        request, 'vous ne pouvez pas investir deux fois avec un même compte')
        else:
            messages.error(request, "vous n'avez pas saisie un montant")

    if request.user.membre:
        return render(request, 'investissement/investi.html', context)


# def investisseur(request):
