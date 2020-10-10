from django import forms
from .models import Post
from tag.models import Tag
from .utils import banned_words_check


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
