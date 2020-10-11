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


class UserForm(forms.ModelForm):
    class Meta:

        model = models.User
        fields = ('username', 'email')

        widgets = {
            'username': forms.DateInput(attrs={'class': 'form-control'}),
            'email': forms.DateInput(attrs={'class': 'form-control'}),

        }

    def clean_username(self):
        name = self.cleaned_data['username']
        if models.User.objects.filter(username=name):
            raise forms.ValidationError(
                "Имя пользователя должно быть уникальным")
        else:
            return name


