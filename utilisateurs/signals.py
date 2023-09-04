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

    # Permet d'ajouter les informations de l'utilisateur dans la table des membres s'il devient membre 
 
    if instance.membre:
        if not Membres.objects.filter(matricule=instance.username).exists():
            Membres.objects.create(
                matricule=instance.username, prenom=instance.first_name, nom=instance.last_name, email=instance.email, phone=instance.phone, adresse=instance.adresse, actif=True)
            
        else:
            member = Membres.objects.get(matricule=instance.username)
            if not member.actif:
                member.actif = True
                member.save()
    else:
        if Membres.objects.filter(matricule=instance.username).exists():
            member = Membres.objects.get(matricule=instance.username)
            member.actif = False
            member.save()
        

