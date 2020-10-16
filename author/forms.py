from django import forms
from .models import Profile
from django.contrib.auth import models


class ProfileForm(forms.ModelForm):
    class Meta:

        model = Profile
        fields = ('date_birth', 'email_hidden')

        widgets = {
            'date_birth': forms.DateInput(attrs={'class': 'form-control'}),
            'email_hidden': forms.CheckboxInput(attrs={'class': 'form-check'})

        }
