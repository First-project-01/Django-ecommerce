from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

PAYMENT_CHOICES = (
    ('C','Credit Card'),
    ('D', 'Debit Card')
)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CheckoutForm(forms.Form):
    phone = forms.CharField(max_length=10)
    address = forms.CharField(max_length=500)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    zip = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    payment = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
