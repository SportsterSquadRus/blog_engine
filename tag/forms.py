from django import forms
from .models import Tag


class TagForm(forms.ModelForm):
    with open('blog/banned_words.txt', encoding='utf8') as file:
        STOP_LIST = file.read().split(', ')
    class Meta:
        model = Tag
        fields = ('tag_title',)

        widgets = {
            'tag_title': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_tag_title(self):
        tagstring = (self.cleaned_data['tag_title']).lower()     
        tags = set((tagstring).split())
        for tag in tags:
            print(tag)
            if tag in self.STOP_LIST:
                raise forms.ValidationError(
                    "Вы позволили себе немного лишнего! Исправьте текст!")
        
        print('its form', tags)
        return tagstring
