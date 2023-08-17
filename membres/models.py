from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()


class Membres(models.Model):
    matricule = models.CharField(max_length=20)
    prenom = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    adresse = models.CharField(max_length=50)
    date_inscris = models.DateTimeField(auto_now_add=True, null=True)
    contribution = models.DecimalField(
        max_digits=12, decimal_places=0, default=0)
    revenue_de_membre = models.DecimalField(
        max_digits=12, decimal_places=0, default=0)

    class Meta:
        verbose_name = "Membre"
        verbose_name_plural = "Membres"

    def __str__(self):
        return self.matricule
