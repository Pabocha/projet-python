from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField, UserChangeForm, AuthenticationForm

User = get_user_model()


class UserCreationForms(UserCreationForm, forms.ModelForm):
    password1 = forms.CharField(
        label="Mot de passe*",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
    )
    password2 = forms.CharField(
        label="mot de passe (à nouveau*)",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirmation du mot de passe'}),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'phone', 'adresse', 'password1', 'password2')

        widgets = {
            # 'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Prenom*',
            'last_name': 'Nom*',
            'email': 'Email*',
            'phone': 'Telephone*',
            'adresse': 'Adresse*'
        }

# class UserLogin(AuthenticationForm):
#     username= forms.CharField(
#         label=("Matricule"),
#         widget=forms.TextInput(
#             attrs={'class': 'form-control mb-2', 'placeholder': 'Matricule'}),
#     )
    
#     password = forms.CharField(
#         label=("Votre mot de passe"),
#         widget=forms.PasswordInput(
#             attrs={'class': 'form-control mb-2', 'placeholder': 'Mot de passe'}),
#     )


 


class MyUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label=("Password"),
        help_text=(
            "Les mots de passe ne peut être modifier que par l'utilisateur en cas d'oublie "
        ),
    )

    class Meta:
        model = User
        fields = "__all__"


class UserChangeForms(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'adresse']

        widgets = {
            # 'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-2'}),
            'phone': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control mb-2'}),
        }

        labels = {
            'first_name': 'Prenom',
            'last_name': 'Nom',
            'email': 'Email',
            'phone': 'Telephone',
            'adresse': 'Adresse'
        }
