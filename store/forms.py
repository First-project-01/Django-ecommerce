from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


SIZES = (
    ('Bunk', 'B'),
    ('Queen', 'Q'),
    ('King', 'K')
)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CheckoutForm(forms.Form):
    phone = forms.CharField(max_length=10, required=True)
    address = forms.CharField(max_length=500, required=True)
    set_default = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)
    zip = forms.CharField(required=True)
    city = forms.CharField(required=True)
    state = forms.CharField(required=True)
