# design1/catalog/forms.py

import regex
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from unidecode import unidecode


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    agree_to_processing = forms.BooleanField(required=True,
                                             widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'agree_to_processing']

    def clean_username(self):
        username = self.cleaned_data['username']

        # Проверка на латиницу и дефис
        if not username.encode('utf-8').isalpha() or '-' in username:
            raise forms.ValidationError('Логин должен содержать только латинские буквы и цифры, без дефисов.')

        # Проверка на уникальность логина
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Такой логин уже занят. Пожалуйста, выберите другой.')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        # Валидация формата email-адреса
        if '@' not in email or '.' not in email:
            raise forms.ValidationError('Некорректный формат email-адреса.')
        return email

    def clean_fio(self):
        fio = self.cleaned_data['fio']

        # Проверка на кириллические буквы, дефис и пробелы
        if not regex.match("^[А-Яа-яЁё\s-]+$", fio):
            raise forms.ValidationError('ФИО должно содержать только кириллические буквы, дефис и пробелы.')

        return fio

    def clean_agree_to_processing(self):
        agree_to_processing = self.cleaned_data['agree_to_processing']
        # Проверка на согласие с обработкой персональных данных
        if not agree_to_processing:
            raise forms.ValidationError('Необходимо согласие с обработкой персональных данных.')
        return agree_to_processing


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['fio']
