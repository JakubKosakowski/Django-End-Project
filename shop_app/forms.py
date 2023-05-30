from django import forms
from django.core.validators import EmailValidator, URLValidator
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    login = forms.CharField(label="Login", min_length=8, max_length=50)
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput, min_length=8, max_length=50)