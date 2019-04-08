from django.shortcuts import render,redirect,reverse
from util.myutil import authuser
from .form import SelfInfoForms
from django.http import JsonResponse,HttpResponse
from blogs.models import User, Category, Keyword, PTArticle
from verify.models import User as YH
from person.models import Article,Comment
from django.core.paginator import Paginator
from django.db import models
import os


# Create your views here.

@authuser
def index(request):
    if request.method == 'GET':
        email = request.session.get('email', None)
        obj = User.objects.filter(email=email).values('username', 'img').first()
        return render(request, "person/index.html", {'email': email, 'obj': obj})


# 个人资料管理
@authuser
def pim(request):
    email = request.session.get('email', None)
    if request.method == 'GET':
        obj = User.objects.filter(email=email).values('username', 'password', 'email', 'tel', 'img').first()
        # form = SelfInfoForms(obj)
        return render(request, "person/pim.html", {'email': email, 'obj': obj})
    if request.is_ajax():
        img = request.FILES.get('img', None)
        # name = os.path.join("media", 'user_img', img.name)
        if img:
            with open('upload/user_img/'+img.name, 'wb+') as f:
                for item in img.chunks():
                    f.write(item)
        return JsonResponse({'status': 'ok', 'src': '/'+os.path.join("media", 'user_img', img.name)})
    if request.method == 'POST':
        username = request.POST.get('username')
        tel = request.POST.get('tel')
        img = request.FILES.get('img', None)
        print(username)
        # img_name = os.path.join("upload", 'user_img', '') + img.name
        # if img:
        #     with open(img_name, 'wb+') as f:
        #         for item in img.chunks():
        #             f.write(item)
        if img:
            with open('upload/user_img/%s' % img.name, 'wb+') as destination:
                for chunk in img.chunks():
                    destination.write(chunk)
            User.objects.filter(email=email).update(username=username, tel=tel, img='/user_img/%s' % img.name)
        return redirect(reverse("person:pim"))


@authuser
def lianjie(request):
    if request.method == 'GET':
        email = request.session.get('email', None)
        return render(request, "person/index.html", {'email': email})


@authuser
def admin(request):
    if request.method == 'GET':
        email = request.session.get('email', None)
        return render(request, "person/index.html", {'email': email})


@authuser
def addArticle(request):
    email = request.session.get('email', None)
    if request.method == 'GET':
        types = Category.getALL()
        keys = Keyword.objects.all()
        return render(request, "person/addArticle.html", {'email': email, 'types': types, 'keys': keys})
    else:
        title = request.POST.get('title', None)
        category = request.POST.get('types', None)
        keys = request.POST.get('keys', None)
        con = request.POST.get('con', None)
        u_id = YH.objects.get(email=email)
        obj = Article(title=title, con=con, c_id=int(category), k_id=int(keys), a_id=int(u_id.id))
        obj.save()
        return redirect(reverse("person:index"))


@authuser
def myArticle(request):
    email = request.session.get('email', None)
    if request.method == 'GET':
        u_id = YH.objects.get(email=email)
        article = Article.objects.filter(a_id=int(u_id.id))
        paginator = Paginator(article, 2)  # Show 25 contacts per page
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        uName = User.objects.filter(email=email).values('username', 'img').first()
        return render(request, "person/myArticle.html", {'email': email, 'article': article, 'uName': uName, 'contacts': contacts})


def showArticle(request, item_id):
    email = request.session.get('email', None)
    if request.method == 'GET':
        u_id = YH.objects.get(email=email)
        first = Article.objects.filter(a_id=int(u_id.id)).first()
        last = Article.objects.filter(a_id=int(u_id.id)).last()
        article = Article.objects.get(id=item_id)
        article_id = Article.objects.filter(a_id=int(u_id.id))
        demo_id = []
        for item in article_id:
            demo_id.append(item.id)
        if str(first.id) == str(item_id):
            last_article = {'title': '到顶了，已无文章------', 'id': item_id}
        else:
            last_article = Article.objects.get(id=demo_id[demo_id.index(item_id)-1])
        if str(last.id) == str(item_id):
            next_article = {'title': '到底了，已无文章------', 'id': item_id}
        else:
            next_article = Article.objects.get(id=demo_id[demo_id.index(item_id)+1])
        uName = User.objects.filter(email=email).values('username', 'img').first()
        pl = Comment.objects.filter(article_id=item_id).order_by('-id')
        for i in pl:
            uname = User.objects.filter(id=i.users_id).first()
            i.users_id = uname
        return render(request, "person/showArticle.html", {'email': email, 'article': article, 'uName': uName, 'last_article': last_article, 'next_article': next_article, 'item_id': item_id, "pl": pl})


# 文章管理程序
def manageArticle(request):
    email = request.session.get("email", None)
    if request.method == 'GET':
        u_id = YH.objects.get(email=email)
        article = Article.objects.filter(a_id=int(u_id.id))
        return render(request, 'person/manageArticle.html', {"article": article})
    if request.is_ajax():
        del_arr = request.POST.getlist('del_arr', None)
        new_del = []
        for item in del_arr:
            new_del.append(int(item))
            Article.objects.filter(id=int(item)).delete()
        return JsonResponse({'status': 'ok'})