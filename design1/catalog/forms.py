# design1/catalog/forms.py
import regex
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from unidecode import unidecode
from .models import UserProfile


@deconstructible
class FIOValidator(validators.RegexValidator):
    regex = r"^[а-яА-Я\s-]+$"
    message = "Enter a valid Full Name. This value may contain only Cyrillic letters, spaces, and dashes."


@deconstructible
class LoginValidator(validators.RegexValidator):
    regex = r"^[a-zA-Z-]+$"
    message = "Enter a valid login. This value may contain only Latin letters and '-'."


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    agree_to_processing = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'agree_to_processing']

    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        validator = LoginValidator()
        try:
            validator(username)
        except ValidationError:
            raise forms.ValidationError(validator.message)

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken. Please choose another one.')

        return username


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['fio']

    fio = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))

    def clean_fio(self):
        fio = self.cleaned_data['fio']
        validator = FIOValidator()
        try:
            validator(fio)
        except ValidationError:
            raise forms.ValidationError(validator.message)
        return fio
