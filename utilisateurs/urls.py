from django.urls import path
from .views import *
from django.contrib.auth import views

urlpatterns = [
    path('register', register, name="register"),
    path('login', logine, name="login"),
    path('compte', compte, name="compte"),
    path('profile', user_profile, name="profile"),
    #    path('getcompte', getcompte, name="getcompte"),
    path('logout', logoute, name="logout"),
    path('activate/<uidb64>/<token>', activate, name="activate"),
    path('reset-password', views.PasswordResetView.as_view(
        template_name="user_auth/password_reset.html"), name="reset_password"),
    path('reset_password_send', views.PasswordResetDoneView.as_view(template_name="user_auth/password_reset_send.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>', views.PasswordResetConfirmView.as_view(template_name="user_auth/password_reset_form.html"),
         name="password_reset_confirm"),
    path('reset_password_complete', views.PasswordResetCompleteView.as_view(template_name="user_auth/password_reset_done.html"),
         name="password_reset_complete")
]
