from django import forms
from verify.models import User
from person.models import Article


class SelfInfoForms(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'username'
            }),
            'img': forms.FileInput(attrs={
                'class': ''
            }),
            'email': forms.TextInput(attrs={
                'class': 'username'
            }),
            'tel': forms.TextInput(attrs={
                'class': 'username'
            })

        }


class ArticleForm(forms.ModelForm):
    class Meta:
        pass
