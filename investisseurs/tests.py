import datetime
from django.test import TestCase
# from .views import *

from django.utils import timezone
from dateutil.relativedelta import relativedelta
from .models import Investisseur, Investissement
from .tasks import augmenter_solde
from django.contrib.auth import get_user_model

User = get_user_model()


class VotreTestCase(TestCase):
    def test_augmenter_solde(self):
        # Créez un investisseur avec les données nécessaires pour le test
        username = "Angelo"
        password = "P@blo 2003"
        solde = 1000
        User.objects.create_user(
            username=username, password=password, solde=solde)
        level = Investissement.objects.create(
            niveau_investissement="VIP 1", montant_min=1500, montant_max=3000)
        investisseur = Investisseur.objects.create(
            matricule=username,
            prenom='lolo',
            nom='voctor',
            email='genie@gmail.com',
            phone="781293098",
            niveau=level,
            montant_investi=1000,
            status_retrait="aucun",
            date_augmentation_solde=timezone.now(),
            # revenue_mensuel=100,
            total_de_gains=0
        )
        investisseur.save()
        date_inscri = timezone.now() - relativedelta(months=+6)

        # Appelez la fonction à tester
        # augmenter_solde()
        investisseur.refresh_from_db()
        mois_ecoules = relativedelta(
            investisseur.date_inscris.date(), date_inscri.date()).months
        # Vérifiez les résultats attendus
        self.assertEqual(mois_ecoules, 6)
        self.assertEqual()

        # self.assertEqual(user.total_de_gains, 100)

        # Assurez-vous que les autres investisseurs n'ont pas été modifiés
        other_users = Investisseur.objects.exclude(pk=investisseur.pk)
        for other_user in other_users:
            self.assertEqual(other_user.total_de_gains, 0)
