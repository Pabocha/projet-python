from django.db.models.signals import post_save, pre_save, pre_delete
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Investisseur
from dateutil.relativedelta import relativedelta
User = get_user_model()


@receiver(post_save, sender=Investisseur)
def change_solde_if_create(sender, instance, created, **kwargs):
    if created:
        user = User.objects.get(username=instance.matricule)
        user.investisseur = True
        user.save()

@receiver(pre_save, sender=Investisseur)
def give_status_investisseur(sender, instance, **kwargs):
    if instance.is_active:
        if not instance.date_inscris:
            instance.date_inscris = timezone.now()
            instance.date_augmentation_solde = timezone.now() + relativedelta(months=+1)
        else:
            pass
        


# verifie si l'investisseur a été supprimer pour pouvoir changer sans statue d'investisseur dans la table utilisateur à None
@receiver(pre_delete, sender=Investisseur)
def change_status_investisseur(sender, instance, **kwargs):
    user = User.objects.get(username=instance.matricule)
    user.investisseur = False
    user.save()

