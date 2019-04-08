from django.db import models
from django.core.validators import RegexValidator

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=12, default='', null=True)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    tel = models.CharField(max_length=11, validators=[
        RegexValidator(regex=r"^1[35687]\d{9}$", message='手机号格式不对！')
    ])
    img = models.ImageField(upload_to="upload/user_img")
    c = models.IntegerField(
        choices=((0, '普通用户'), (1, '高级用户')), default=0
    )
    flower = models.TextField(max_length=65535, default='')
    star = models.TextField(max_length=65535, default='')

    def __str__(self):
        return self.username