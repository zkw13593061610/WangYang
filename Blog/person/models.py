from django.db import models
from blogs.models import PTArticle,Category,Keyword
from verify.models import User
from ckeditor.fields import RichTextField
# Create your models here.


class Article(models.Model):
    c = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name='分类')
    k = models.ForeignKey(to=Keyword, on_delete=models.CASCADE, verbose_name='关键字')
    a = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="作者", null=True)
    title = models.CharField(max_length=32, verbose_name='文章标题')
    con = RichTextField()
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='发布日期')
    u_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')
    status = models.BooleanField(default=False, verbose_name="发布状态")
    look = models.IntegerField(default=0)


class Comment(models.Model):
    con = models.TextField(max_length=2048, verbose_name='评论内容')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='评论的日期')
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, verbose_name='对应的博客文章')
    users = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='评论者')

