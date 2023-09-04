from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.contrib.auth.models import AbstractUser
import os

# Create your models here.


def rename_image(instance, filename):
    upload_to = 'media/'
    extension = filename.split('.')[-1]

    if instance.first_name:
        filename = (f"{instance.first_name}.{extension}")
        return os.path.join(upload_to, filename)


class Utilisateur(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',  # Exemple : +33612345678
        message="Le numéro de téléphone doit être au format '+33612345678'."
    )

   
    phone = models.CharField(validators=[phone_regex], max_length=17, error_messages={
                             'required': 'Ce champ est obligatoire.', 'invalid': 'Votre numéro de téléphone ne doit pas contenir des espaces.'})
    email = models.EmailField(verbose_name='email address', validators=[
                              EmailValidator(message='Entre une adresse mail valide.')], unique=True)
    image_de_profile = models.ImageField(upload_to=rename_image, blank=True)
    adresse = models.CharField(max_length=30, null=True)
    membre = models.BooleanField(default=False)
    investisseur = models.BooleanField(default=False)


class UserCounter(models.Model):
    value = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.value)


class Notification(models.Model):
    TYPE_CHOICES = [
        ('inscription', 'Inscription'),
        ('retrait', 'Demande de retrait'),
        ('investissement', 'Investissement')
    ]
    matricule = models.CharField(max_length=50)
    nom = models.CharField(max_length=75)
    prenom = models.CharField(max_length=75)
    email = models.EmailField()
    message = models.TextField()
    type_message = models.CharField(max_length=50, choices=TYPE_CHOICES)
    read = models.BooleanField(default=False)
    date_ajouter = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_ajouter',)

    def __str__(self):
        return self.nom
