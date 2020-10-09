from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:

        model = Profile
        fields = ('date_birth',)

        widgets = {
            'title': forms.DateInput(attrs={'class': 'form-control'})
        }
