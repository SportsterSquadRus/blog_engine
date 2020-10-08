from django import forms
from .models import Post
from taggit.forms import TagWidget


class PostForm(forms.ModelForm):
    STOP_LIST = [
                'блядь',
                'бляди',
                'пизда',
                'пиздец',
            ]
    class Meta:
        model = Post
        fields = ('title', 'body', 'cover_url', 'draft_status', 'tags')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'cover_url': forms.URLInput(attrs={'class': 'form-control'}),
            'draft_status': forms.CheckboxInput(attrs={'class': 'form-check'}),
            'tags': TagWidget(attrs={'class': 'form-control'}),
        }

    def clean_body(self):        
        text = self.cleaned_data['body']
        for word in self.STOP_LIST:
            if word in text:
                raise forms.ValidationError("Вы позволили себе немного лишнего! Исправьте текст!")
        return text
    
    def clean_title(self):        
        text = self.cleaned_data['title']
        for word in self.STOP_LIST:
            if word in text:
                raise forms.ValidationError("Вы позволили себе немного лишнего! Исправьте текст!")
        return text

    def clean_tags(self):        
        text = self.cleaned_data['tags']
        for word in self.STOP_LIST:
            if word in text:
                raise forms.ValidationError("Вы позволили себе немного лишнего! Исправьте текст!")
        return text
