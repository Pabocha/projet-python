from django.contrib import admin
from .models import Membres
from django.contrib.auth.admin import UserAdmin
# from utilisateurs.models import uT

# Register your models here.


class MemberAdmin(admin.ModelAdmin):
    list_display = ['matricule', 'prenom',
                    'nom', 'contribution', 'date_inscris', 'actif']
    search_fields = ('matricule', 'prenom', 'nom', 'email',)
    list_filter = ('matricule', 'date_inscris')


admin.site.register(Membres, MemberAdmin)
