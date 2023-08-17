from django.contrib import admin
from .models import Contacts

# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "read", "date_envoie")
    list_filter = ("date_envoie", )
    search_fields = ("name", "email", "subject", )


admin.site.register(Contacts, ContactAdmin)
