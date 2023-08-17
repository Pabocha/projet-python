import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from investisseurs.models import Investisseur
from membres.models import Membres
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.utils import timezone
from utilisateurs.models import Notification
from contacts.models import Contacts
from django.contrib.admin.views.decorators import user_passes_test

User = get_user_model()


def home(request):
    return render(request, 'base/index.html')


def about(request):
    return render(request, 'base/about.html')


def profil(request):
    return render(request, 'user_auth/profil.html')


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    # pour les notifications
    notification = Notification.objects.filter(read=False)
    count_notifications = notification.count()

    # pour les investisseur
    nbre_total_investisseur = Investisseur.objects.count()
    somme_montant_investi = Investisseur.objects.aggregate(
        total_montant=Sum('montant_investi'))['total_montant']
    user_retrait_en_attente = Investisseur.objects.filter(
        retrait_en_attente__gt=0)

    # pour les contacts
    contact_no_read = Contacts.objects.filter(read=False)
    count_contact = contact_no_read.count()

    # Pour le membres
    nbre_total_membres = Membres.objects.count()
    contribution_total_membres = Membres.objects.aggregate(total_contribution=Sum('contribution'))['total_contribution']

    if request.method == 'POST':

        # Récupère la période sélectionnée depuis le formulaire
        selected_period = request.POST.get('period')
        # Convertir la valeur stockée en un objet conscient du fuseau horaire
        today = timezone.localdate()

        # pour filtrer rêquete par rapport aux jours
        match selected_period:

            case "today_investisseur":
                nbre_total_investisseur = Investisseur.objects.filter(
                    date_inscris__gte=today).count()
            case "this_month_investisseur":
                start_date = timezone.make_aware(
                    datetime.datetime(today.year, today.month, 1))
                nbre_total_investisseur = Investisseur.objects.filter(
                    date_inscris__gte=start_date).count()
            case "this_year_investisseur":
                start_date = timezone.make_aware(
                    datetime.datetime(today.year, 1, 1))
                nbre_total_investisseur = Investisseur.objects.filter(
                    date_inscris__gte=start_date).count()

            case "today_investissement":
                if Investisseur.objects.filter(date_inscris__gte=today).exists():
                    somme_montant_investi = Investisseur.objects.filter(date_inscris__gte=today).aggregate(
                        total_montant=Sum('montant_investi'))['total_montant']
                else:
                    somme_montant_investi = 0
            case "this_month_investissement":
                start_date = timezone.make_aware(
                    datetime.datetime(today.year, today.month, 1))
                if Investisseur.objects.filter(date_inscris__gte=start_date).exists():
                    somme_montant_investi = Investisseur.objects.filter(date_inscris__gte=start_date).aggregate(
                        total_montant=Sum('montant_investi'))['total_montant']
                else:
                    somme_montant_investi = 0
            case "this_year_investissement":
                start_date = timezone.make_aware(
                    datetime.datetime(today.year, 1, 1))
                if Investisseur.objects.filter(date_inscris__gte=start_date).exists():
                    somme_montant_investi = Investisseur.objects.filter(date_inscris__gte=start_date).aggregate(
                        total_montant=Sum('montant_investi'))['total_montant']
                else:
                    somme_montant_investi = 0
        if 'form_retrait' in request.POST:
            matricule_investisseur = request.POST['matricule_investisseur']
            investisseur = Investisseur.objects.get(
                matricule=matricule_investisseur)
            investisseur.total_de_retrait += investisseur.retrait_en_attente
            investisseur.retrait_en_attente = 0
            investisseur.status_retrait = "aucun"
            investisseur.save()

        elif 'form_rejet_retrait' in request.POST:
            matricule_investisseur = request.POST['matricule_investisseur']
            investisseur = Investisseur.objects.get(
                matricule=matricule_investisseur)
            investisseur.solde += investisseur.retrait_en_attente
            investisseur.retrait_en_attente = 0
            investisseur.status_retrait = "aucun"
            investisseur.save()


    context = {
        'nbre_total_investisseur': nbre_total_investisseur,
        'somme_montant_investi': somme_montant_investi,
        'user_retrait_en_attente': user_retrait_en_attente,
        'notifications': notification,
        'count': count_notifications,
        'contacts': contact_no_read,
        'count_contact': count_contact,
        'nbre_total_membres': nbre_total_membres,
        'contribution_total_membres': contribution_total_membres,

    }
    return render(request, 'base/dashboard.html', context)


def viewAllNotifications(request):
    all_notifications_no_read = Notification.objects.filter(read=False)
    all_notifications_read = Notification.objects.filter(read=True)
    if request.method == 'POST':
        if 'btn_delete_all' in request.POST:
            selected_ids = request.POST.getlist('selected_items')
            Notification.objects.filter(pk__in=selected_ids).delete()
        elif 'btn_view' in request.POST:
            id_user = request.POST['id_message_user_no_read']
            user = Notification.objects.get(id=id_user)
            user.read = True
            user.save()
        elif 'delete_message' in request.POST:
            id_user = request.POST['id_message']
            user = Notification.objects.get(id=id_user)
            user.delete()
    context = {
        'notification_no_read': all_notifications_no_read,
        'notification_read': all_notifications_read,
    }
    return render(request, 'investissement/notification.html', context)


def handel404(request, exception):
    return render(request, 'base/404.html')
