import time
# pour exécuter les tâches en arrière plan
from celery import shared_task

from .models import Investisseur
from django.utils import timezone

# pour gerer les mois ecoulé et aussi ajouter 1 mois de plus à date_augmentation_solde
from dateutil.relativedelta import relativedelta
# from celery.decorators import periodic_task


@shared_task
def augmenter_solde():
    users = Investisseur.objects.all()
    # boucle permettant d'augmenter le solde des investisseurs chaque mois pendant 5 minutes

    for user in users:
        # permet de verifier si date à laquelle le solde dois augmenter est égale à la date actuel
        if user.is_active:
            if timezone.localtime(user.date_augmentation_solde).date() <= timezone.now().date():
                mois_ecoules = relativedelta(
                    timezone.now().date(), user.date_inscris.date()).months
                if mois_ecoules <= 5:
                    user.solde += user.revenue_mensuel
                    user.date_augmentation_solde = user.date_augmentation_solde + relativedelta(months=+1)
                    Investisseur.objects.filter(pk=user.pk).update(
                        solde=user.solde,
                        date_augmentation_solde=user.date_augmentation_solde,
                    )
                else:
                    user.is_active = False
                    Investisseur.objects.filter(pk=user.pk).update(
                        is_active=False
                    )
        else:
            pass
