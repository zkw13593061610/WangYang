from django.forms import Form,ModelForm,Widget,models
import datetime
from django import forms
from .models import User
from captcha.fields import CaptchaField
from django.core.validators import ValidationError
from django.contrib.auth.hashers import make_password,check_password
import hashlib


class RegisterForm(ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        tel = cleaned_data.get('tel', None)
        email = cleaned_data.get('email', None)
        password = cleaned_data.get('password', None)
        new_temp = password[0:len(password) - 1]
        m = hashlib.md5()
        m.update(new_temp.encode('utf-8'))
        sign = m.hexdigest()
        cleaned_data['password'] = sign
        if tel and email:
            is_tel_exist = User.objects.filter(tel=tel).first()
            is_email_exist = User.objects.filter(email=email).first()
            if is_email_exist and is_tel_exist:
                raise ValidationError('该手机号和邮箱都已被人注册过了')
            if is_email_exist:
                raise ValidationError('该邮箱已被人注册过了')
            if is_tel_exist:
                raise ValidationError('该手机号已被人注册过了')

    class Meta:
        model = User
        exclude = ['img', 'c', 'flower', 'star']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'username',
                'placeholder': '请输入用户名'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'username',
                'placeholder': '请输入密码'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'username',
                'placeholder': '请输入邮箱号'
            }),
            'tel': forms.TextInput(attrs={
                'class': 'username',
                'placeholder': '请输入手机号'
            })
        }
        labels = {
            'username': '请输入用户名',
            'password': '请输入密码',
            'email': '请输入邮箱',
            'tel': '请输入手机号'
        }


class LoginForm(ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = User
        exclude = ['username']
        fields = ['password', 'email', 'captcha']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'username',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'username',
                'placeholder': '请输入密码'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'username',
                'placeholder': '请输入邮箱'
            }),
            'captcha': forms.TextInput(attrs={
                'class': 'username',
                'placeholder': '请输入右侧验证码'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email', None)
        password = cleaned_data.get('password', None)
        # print(password,make_password(password))
        new_temp = password[0:len(password) - 1]
        m = hashlib.md5()
        m.update(new_temp.encode('utf-8'))
        sign = m.hexdigest()
        password = sign
        # cleaned_data['password'] = make_password(password)
        # cleaned_data['password'] = check_password(password)
        if email and password:
            res = User.objects.filter(email=email, password=password).first()
            if not res:
                raise ValidationError('登录失败')

