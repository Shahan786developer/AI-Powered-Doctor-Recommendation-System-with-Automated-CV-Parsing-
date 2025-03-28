# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from resume.models import CV

class CVUploadForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['cv_file']


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-control username-field',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control password-field',
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-control username-field',
            'style': 'padding-left: 35px; border: 1px solid #196e96; border-radius: 4px; background-color: #f9f9f9;'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control password-field',
            'style': 'padding-left: 35px; border: 1px solid #196e96; border-radius: 4px; background-color: #f9f9f9;'
        })
    )

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-control username-field',
            'style': 'padding-left: 35px; border: 1px solid #196e96; border-radius: 4px; background-color: #f9f9f9;'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control password-field',
            'style': 'padding-left: 35px; border: 1px solid #196e96; border-radius: 4px; background-color: #f9f9f9;'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class': 'form-control password-field',
            'style': 'padding-left: 35px; border: 1px solid #196e96; border-radius: 4px; background-color: #f9f9f9;'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
