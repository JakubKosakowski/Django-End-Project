from django import forms
from django.contrib.auth.models import User
from django.core.validators import EmailValidator, URLValidator
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    """Formularz logowania do aplikacji"""
    login = forms.CharField(label="Login")
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    """Formularz rejestracji do aplikacji"""
    first_name = forms.CharField(label="Imię")
    last_name = forms.CharField(label="Nazwisko")
    username = forms.CharField(label="Login", min_length=5, max_length=30)
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput, min_length=5, max_length=30)
    password_rep = forms.CharField(label="Hasło ponownie", widget=forms.PasswordInput, min_length=5, max_length=30)
    email = forms.CharField(label="Email", widget=forms.EmailInput, validators=[EmailValidator()])
    street = forms.CharField(label="Ulica i numer domu", max_length=60)
    postal_code = forms.CharField(label="Kod pocztowy", max_length=20)
    city = forms.CharField(label="Miasto", max_length=60)
    country = forms.CharField(label="Państwo", max_length=50)

    def clean(self):
        data = super().clean()
        if User.objects.filter(username=data['username']) or User.objects.filter(email=data['email']):
            raise forms.ValidationError('Użytkownik o takiej nazwie lub tym adresie email już istnieje')
        if data['password'] != data['password_rep']:
            raise forms.ValidationError('Wprowadzone hasła nie pasują do siebie')
        return data


class ChangePasswordForm(forms.Form):
    """Formularz do zmiany hasła użytownika"""
    new_password = forms.CharField(label="Nowe hasło", widget=forms.PasswordInput)
    repeat_new_password = forms.CharField(label="Powtórz nowe hasło", widget=forms.PasswordInput)
