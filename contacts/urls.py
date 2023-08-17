from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact, name="contact"),
    path('dashboard/message/', views.viewContact, name="viewContact"),
]
