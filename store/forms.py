from django import forms
from .models import Customer
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Customer
        fields = ['username', 'email', 'password1', 'password2']