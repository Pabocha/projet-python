from django.db.models.signals import post_save, pre_save
from django.db import transaction
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from membres.models import Membres
from .models import UserCounter
from investisseurs.models import Investisseur
from .models import Notification

User = get_user_model()


@receiver(pre_save, sender=User)
def change_membre(sender, instance, **kwargs):
    # Permet de créer le matricule de l'utilisateur
    if instance.username == "":
        with transaction.atomic():
            counter, created = UserCounter.objects.select_for_update().get_or_create()
            counter.value += 1
            counter.save()
        id = counter.value
        firstname = instance.first_name[:3].upper()
        lastname = instance.last_name[:3].upper()
        date_inscris = instance.date_joined.strftime('%m-%y')
        instance.username = (f"00{id}-{firstname}{lastname}-{date_inscris}")

        Notification.objects.create(matricule=instance.username, nom=instance.last_name, prenom=instance.first_name, email=instance.email,
                                    message="Un nouvel utilisateur s'est inscris sur la plateforme", type_message="inscription")

    # Permet de savoir si l'utilisateur à payé l'inscription pour devenir membre si c'est valide automatiquement il devient membre
    if instance.inscription == None:
        pass
    elif instance.inscription >= 10000:
        instance.membre = True
        if not Membres.objects.filter(matricule=instance.username).exists():
            obj = Membres.objects.create(
                matricule=instance.username, prenom=instance.first_name, nom=instance.last_name, email=instance.email, phone=instance.phone, adresse=instance.adresse)
            obj.save()
        else:
            pass
