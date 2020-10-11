from django import forms
from .models import Post
from .utils import banned_words_check
from allauth.account.forms import LoginForm, SignupForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'cover_url', 'draft_status')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'cover_url': forms.URLInput(attrs={'class': 'form-control'}),
            'draft_status': forms.CheckboxInput(attrs={'class': 'form-check'}),
        }

    def clean_body(self):
        text = (self.cleaned_data['body']).lower()
        return banned_words_check(text)

    def clean_title(self):
        text = (self.cleaned_data['title']).lower()
        return banned_words_check(text)




class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['remember'].widget = forms.CheckboxInput(attrs={'class': 'form-check'})

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['email'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['password1'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['password2'].widget = forms.TextInput(attrs={'class': 'form-control'})

