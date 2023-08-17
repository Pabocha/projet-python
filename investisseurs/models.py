from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

# Create your models here.
User = get_user_model()


class Investissement(models.Model):
    niveau_investissement = models.CharField(
        max_length=50, unique=True, verbose_name="Niveau")
    montant_min = models.DecimalField(max_digits=12, decimal_places=0)
    montant_max = models.DecimalField(max_digits=12, decimal_places=0)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.niveau_investissement)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.niveau_investissement


class Investisseur(models.Model):

    retrait = [
        ('approuvé', 'Approuvé'),
        ('attente', 'Attente'),
        ('rejeté', 'rejeté'),
        ('aucun', 'aucun')
    ]

    matricule = models.CharField(max_length=20)
    prenom = models.CharField(max_length=70)
    nom = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    niveau = models.ForeignKey(Investissement, on_delete=models.CASCADE)
    montant_investi = models.DecimalField(
        max_digits=12, decimal_places=0, null=True, default=0)
    revenue_mensuel = models.DecimalField(
        max_digits=12, decimal_places=0, blank=True, null=True, default=0)
    solde = models.DecimalField(
        max_digits=12, decimal_places=0, blank=True, null=True, default=0)
    total_de_gains = models.DecimalField(
        max_digits=12, decimal_places=0, blank=True, null=True, default=0)
    retrait_en_attente = models.DecimalField(
        max_digits=12, decimal_places=0, blank=True, null=True, default=0)
    total_de_retrait = models.DecimalField(
        max_digits=12, decimal_places=0, blank=True, null=True, default=0)
    status_retrait = models.CharField(
        max_length=50, choices=retrait, default='aucun')
    is_active = models.BooleanField(default=False)
    date_inscris = models.DateTimeField(null=True, blank=True)
    date_augmentation_solde = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Investisseur"
        verbose_name_plural = "Investisseurs"

    def __str__(self):
        return self.matricule

    def save(self, *args, **kwargs):
        self.revenue_mensuel = (self.montant_investi * 15)/100
        super().save(*args, **kwargs)
