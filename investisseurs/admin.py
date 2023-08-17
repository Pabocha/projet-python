from django.contrib import admin
from .models import *

# Register your models here.


class InvestissementAdmin(admin.ModelAdmin):

    list_display = ["niveau_investissement", "montant_min", "montant_max"]

    search_fields = ("niveau_investissement",)
    list_filter = ('niveau_investissement', 'montant_min', 'montant_max', )


class InvestisseurAdmin(admin.ModelAdmin):

    list_display = ['matricule', 'prenom',
                    'niveau', 'montant_investi', 'revenue_mensuel', 'date_inscris', 'date_augmentation_solde']

    list_filter = ('niveau', 'date_inscris',)
    search_fields = ("matricule", "prenom", "email", "nom",)


admin.site.register(Investissement, InvestissementAdmin)
admin.site.register(Investisseur, InvestisseurAdmin)
