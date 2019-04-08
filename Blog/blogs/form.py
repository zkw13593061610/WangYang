from django import forms
from .models import UserInfo


class UserInfoForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        exclude = ['sh']
        model = UserInfo
        widgets = {
            'u': forms.HiddenInput(),
            'company': forms.TextInput(attrs={
                'class': 'username',
                'placeholder': '请输入公司名'
            }),
            'position': forms.TextInput(attrs={
                'class': 'username',
                'placeholder': '输入你的职称'
            }),
            'hobby': forms.TextInput(attrs={
                'class': 'username',
                'placeholder': '输入你兴趣爱好'
            }),
            'why': forms.Textarea(attrs={
                'class': 'username',
                'placeholder': '请输入......'
            }),
            'realName': forms.TextInput(attrs={
                'class': 'username',
                'placeholder': '请输入真实姓名'
            }),
        }