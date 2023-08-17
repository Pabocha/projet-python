from django.contrib import admin
from .models import Utilisateur, UserCounter, Notification
from .forms import UserCreationForms, MyUserChangeForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class AdminUser(UserAdmin):
    add_form = UserCreationForms
    form = MyUserChangeForm

    list_display = ['username', 'first_name',
                    'last_name', 'email', 'is_active', 'membre', 'investisseur']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Info Personnel', {'fields': ('first_name',
         'last_name', 'email', 'phone', 'adresse', 'image_de_profile')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Inscription', {'fields': ('inscription', 'membre')}),
        ('Investissement', {
         'fields': ('investisseur',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'phone', 'adresse'),
        }),
    )
    list_filter = ('membre', 'investisseur', 'is_staff',
                   'is_superuser', 'is_active',)
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('date_joined',)
    filter_horizontal = ('groups', 'user_permissions',)


class AdminNotif(admin.ModelAdmin):
    list_display = ['matricule', 'nom', 'prenom', 'email',
                    'type_message',  'date_ajouter', 'read']
    list_filter = ['date_ajouter', 'type_message']
    search_fields = ('matricule', 'nom', 'email', 'type_message',)


admin.site.register(Utilisateur, AdminUser)
admin.site.register(UserCounter)
admin.site.register(Notification, AdminNotif)
