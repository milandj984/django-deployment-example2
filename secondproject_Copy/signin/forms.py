from django import forms
from django.contrib.auth.models import User
from .models import UserProfileInfo


class UserForm(forms.ModelForm):
    # Stilizujes svako polje
    password = forms.CharField(widget=forms.PasswordInput({'placeholder': 'password', 'class': 'form-control'}))

    class Meta():
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']


class UserProfileInfoForm(forms.ModelForm):
    # portfolio_site = forms.URLField(required=False)
    # profile_picture = forms.ImageField(required=False)

    class Meta():
        model = UserProfileInfo
        exclude = ['user']