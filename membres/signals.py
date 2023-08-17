from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from .models import Membres
from django.contrib.auth import get_user_model
User = get_user_model()

# User = get_user_model


@receiver(pre_delete, sender=Membres)
def change_member_false(sender, instance, **kwargs):
    if User.objects.filter(username=instance.user).exists():
        user = User.objects.get(username=instance.user)
        user.inscription = 0
        user.membre = False
        user.save()
    else:
        pass
