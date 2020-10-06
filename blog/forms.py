from django import forms
from .models import Post, Comment
from taggit.forms import TagWidget


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'cover_url', 'draft_status', 'tags')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'cover_url':forms.URLInput(attrs={'class': 'form-control'}),
            'draft_status': forms.CheckboxInput(attrs={'class': 'form-check'}),
            'tags': TagWidget(attrs={'class': 'form-control'}),
        }