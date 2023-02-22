from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms
from myapp.models import User, Purchase, Return


class UserCreateForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput)
    email = forms.EmailField(widget=forms.EmailInput)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    cash = forms.DecimalField(initial=10000, widget=forms.HiddenInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'cash')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email is already registered')
        return email

class PurchaseCreateForm(forms.ModelForm):
    available = forms.IntegerField(initial=1, widget=forms.NumberInput(attrs={'min': 1}))

    class Meta:
        model = Purchase
        fields = ['available']


class ReturnCreateForm(forms.ModelForm):
    purchase = forms.ModelChoiceField(queryset=Purchase.objects.all(), required=False, widget=forms.HiddenInput)

    class Meta:
        model = Return
        fields = ['purchase']

