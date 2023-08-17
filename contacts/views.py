from immobilier import settings
from django.shortcuts import render, redirect
from .models import Contacts
from django.contrib import messages
'''importation d'envoi de mail'''
from django.core.mail import send_mail
'''importation de la configuration des paramettre de mail'''

# Create your views here.


def contact(request):

    if request.method == 'POST':
        name_user = request.POST['name']
        email_user = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        obj = Contacts.objects.create(
            name=name_user, email=email_user, subject=subject, message=message)
        obj.save()
        messages.success(
            request, 'votre message à été reçu vous aurez une réponse dans maximum 24h par email soyer connecter')

        '''envoi de mail'''
        send_message = (
            f"Objet: {subject}\n\n email: {email_user}\n\nNom: {name_user}\n\n {message}\n\n")
        to_list = ['davidkiba88@gmail.com', 'Ppabocha03@gmail.com']
        send_mail("Coopérative construisons ensemble",
                  send_message, settings.EMAIL_HOST_USER, to_list)

        return redirect('contact')

    return render(request, 'base/contact.html')


def viewContact(request):
    contact_no_read = Contacts.objects.filter(read=False)
    contact_read = Contacts.objects.filter(read=True)

    if request.method == "POST":
        if 'btn_delete_all' in request.POST:
            selected_ids = request.POST.getlist('selected_items')
            Contacts.objects.filter(pk__in=selected_ids).delete()
        elif 'btn_view' in request.POST:
            id_user = request.POST['id_message_user_no_read']
            contact = Contacts.objects.get(id=id_user)
            contact.read = True
            contact.save()
        elif 'delete_message' in request.POST:
            id_user = request.POST['id_message']
            contact = Contacts.objects.get(id=id_user)
            contact.delete()
    context = {'contact_no_read': contact_no_read,
               'contact_read': contact_read,
               }
    return render(request, 'investissement/message.html', context)
