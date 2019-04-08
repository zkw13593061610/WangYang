from django.db import models
from django.utils.html import format_html, SafeText
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=16, verbose_name='分类')

    def listKeyword(self):
        objs = self.keyword_set.all()
        arr = []
        for obj in objs:
            arr.append("<e style='margin:0 8px;color:red'>"+obj.name+"<e>")
        return SafeText(''.join(arr))
        # return format_html(''.join(arr))
    listKeyword.short_description = "关键字"

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类管理'

    def __str__(self):
        return self.name

    @classmethod
    def getALL(cls):
        return cls.objects.all()


class Keyword(models.Model):
    name = models.CharField(max_length=20, verbose_name='分类的关键字')
    c = models.ForeignKey(to=Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PTArticle(models.Model):
    c = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name='分类')
    k = models.ForeignKey(to=Keyword, on_delete=models.CASCADE, verbose_name='关键字')
    a = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='作者', null=True)
    title = models.CharField(max_length=32, verbose_name='文章标题')
    # con = models.TextField(max_length=10240, verbose_name='文章内容')
    con = RichTextField()
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='发布日期')
    u_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')

    class Meta:
        verbose_name = '文章标题'
        verbose_name_plural = '文章管理'

    @classmethod
    def getALL(cls):
        return cls.objects.all()


from verify.models import User


class UserInfo(models.Model):
    u = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name='博客平台用户', null=True, default='')
    company = models.CharField(max_length=30, verbose_name='公司', default='')
    position = models.CharField(max_length=30, verbose_name='职位', default='')
    hobby = models.CharField(max_length=120, verbose_name='爱好',default='')
    why = models.CharField(max_length=1024, verbose_name='申请理由',default='')
    realName = models.CharField(max_length=20, verbose_name='真实姓名',default='')
    sh = models.IntegerField(choices=((0, '未审核'), (1, '审核中'), (2, '审核通过')), default=1)

    # def __str__(self):
    #     return self.u

    def sh_statues(self):
        num = self.sh
        statue = ''
        color = ''
        if num == 0:
            statue = '未申请'
            color = '#000'
        elif num == 1:
            statue = '审核中'
            color = 'red'
        elif num == 2:
            statue = '审核通过'
            color = 'green'
        tem = "<span style='color:%s'>%s</span>" % (color, statue)
        return SafeText(tem)

    class Meta:
        verbose_name = '开通用户信息'
        verbose_name_plural = '用户管理'










