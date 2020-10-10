
from django import forms
from .models import Profile
from django.contrib.auth import models


class ProfileForm(forms.ModelForm):
    class Meta:

        model = Profile
        fields = ('date_birth',)

        widgets = {
            'date_birth': forms.DateInput(attrs={'class': 'form-control'})
        }


class UserForm(forms.ModelForm):
    class Meta:

        model = models.User
        fields = ('username', 'email')

        widgets = {
            'username': forms.DateInput(attrs={'class': 'form-control'}),
            'email': forms.DateInput(attrs={'class': 'form-control'}),

        }
