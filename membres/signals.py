from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from .models import Membres
from django.contrib.auth import get_user_model
User = get_user_model()

# User = get_user_model


@receiver(pre_delete, sender=Membres)
def change_member_false(sender, instance, **kwargs):
    if User.objects.filter(username=instance.matricule).exists():
        user = User.objects.get(username=instance.matricule)
        user.membre = False
        user.save()
    else:
        pass

# @receiver(pre_save, sender=User)
# def member_is_actif(sender, instance, **kwargs):
#     if Membres.objects.filter(matricule=instance.username).exists():
#         member = Membres.objects.get(matricule=instance.username)
#         if instance.membre == False and member.actif == False:
#             member.actif = True
#             member.save()
        

        