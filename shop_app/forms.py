from django import forms
from django.core.validators import EmailValidator, URLValidator
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    login = forms.CharField(label="Login")
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)