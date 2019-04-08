from django.shortcuts import render, redirect, reverse, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Keyword, Category, PTArticle, UserInfo
from verify.form import User
from verify.models import User as YH
from person.models import Article,Comment
from .form import UserInfoForm
from django.core.paginator import Paginator

# Create your views here.


# 网站主页处理程序
def index(request):
    if request.method == 'GET':
        data = Category.getALL()
        # article = PTArticle.getALL()
        article = PTArticle.objects.filter(a_id=1)
        email = request.session.get('email', None)
        if email:
            kt_id = User.objects.get(email=email)
            KT = UserInfo.objects.filter(u=int(kt_id.id)).first()
            if KT:
                statue = KT.sh
            else:
                statue = 3
        else:
            statue = 0
        uName = User.objects.filter(email=email).values('username', 'img').first()
        for item in data:
            all_Art = item.id
            item.all_Art = PTArticle.objects.filter(c_id=all_Art)
            num = 1
            for it in item.all_Art:
                it.sort = num
                num += 1
            print(item.all_Art)
        paginator = Paginator(article, 5)  # Show 25 contacts per page
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        return render(request, "polls/index.html", {'category': data, 'con': article, 'email': email, 'uName': uName, 'statue': statue,'contacts': contacts})


@csrf_exempt
def getKeyword(request):
    if request.is_ajax():
        c = request.POST.get('c', None)
        res = Keyword.objects.filter(c=c).values_list('id', 'name')
        obj = {}
        for arr in res:
            obj[arr[0]] = arr[1]
        return JsonResponse(obj)


# 开通博客处理程序
def kaitong(request):
    if request.method == 'GET':
        email = request.session.get('email', None)
        form = UserInfoForm()
        if email:
            obj = User.objects.filter(email=email).first()
            c = obj.c
            if int(c) == 0:
                form = UserInfoForm({'u': obj.id, 'sh': 1})
                return render(request, 'polls/kaitong.html', {'form': form})
            else:
                return HttpResponse('用户后台')
        else:
            return render(request, 'polls/kaitong.html', {'form': form})
    else:
        form = UserInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("blogs:index"))
        else:
            return render(request, 'polls/kaitong.html')


# 平台文章展示处理程序
def my_blog(request):
    if request.method == 'GET':
        data = Category.getALL()
        article = Article.objects.all()
        email = request.session.get('email', None)
        paginator = Paginator(article, 5)  # Show 25 contacts per page
        page = request.GET.get('page')
        contacts = paginator.get_page(page)
        uName = User.objects.filter(email=email).values('username', 'img').first()
        return render(request, "polls/my_blog.html", {'category': data, 'con': article, 'email': email,'contacts': contacts, 'uName': uName})


# 平台文章具体内容展示程序
def blog_show(request, item_id):
    email = request.session.get('email', None)
    if email:
        if request.method == 'GET':
            # u_id = YH.objects.get(email=email)
            first = Article.objects.first()
            last = Article.objects.last()
            article = Article.objects.get(id=item_id)
            article_id = Article.objects.all()
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
            return render(request, "polls/blog_show.html", {'email': email, 'article': article, 'uName': uName, 'last_article': last_article, 'next_article': next_article, 'item_id': item_id, 'pl': pl})
        if request.is_ajax():
            user_id = YH.objects.get(email=email)
            article_id = item_id
            con = request.POST.get('con', None)
            obj = Comment(con=con, article_id=int(article_id), users_id=int(user_id.id))
            obj.save()
            return JsonResponse({"statue": 'ok'})
    else:
        first = Article.objects.first()
        last = Article.objects.last()
        article = Article.objects.get(id=item_id)
        article_id = Article.objects.all()
        demo_id = []
        for item in article_id:
            demo_id.append(item.id)
        if str(first.id) == str(item_id):
            last_article = {'title': '到顶了，已无文章------', 'id': item_id}
        else:
            last_article = Article.objects.get(id=demo_id[demo_id.index(item_id) - 1])
        if str(last.id) == str(item_id):
            next_article = {'title': '到底了，已无文章------', 'id': item_id}
        else:
            next_article = Article.objects.get(id=demo_id[demo_id.index(item_id) + 1])
        pl = Comment.objects.filter(article_id=item_id).order_by('-id')
        for i in pl:
            uname = User.objects.filter(id=i.users_id).first()
            i.users_id = uname
        return render(request, "polls/blog_show.html",
                      {'email': email, 'article': article, 'last_article': last_article,
                       'next_article': next_article, 'item_id': item_id, 'pl': pl})

# 平台文章详情显示


def PT_blog_show(request, item_id):
    email = request.session.get('email', None)
    if email:
        if request.method == 'GET':
            first = PTArticle.objects.first()
            last = PTArticle.objects.last()
            article = PTArticle.objects.get(id=item_id)
            article_id = PTArticle.objects.all()
            demo_id = []
            for item in article_id:
                demo_id.append(item.id)
            if str(first.id) == str(item_id):
                last_article = {'title': '到顶了，已无文章------', 'id': item_id}
            else:
                last_article = PTArticle.objects.get(id=demo_id[demo_id.index(item_id) - 1])
            if str(last.id) == str(item_id):
                next_article = {'title': '到底了，已无文章------', 'id': item_id}
            else:
                next_article = PTArticle.objects.get(id=demo_id[demo_id.index(item_id) + 1])
            uName = User.objects.filter(email=email).values('username', 'img').first()
            pl = Comment.objects.filter(article_id=item_id).order_by('-id')
            for i in pl:
                uname = User.objects.filter(id=i.users_id).first()
                i.users_id = uname
            return render(request, "polls/PT_blog_show.html",
                          {'email': email, 'article': article, 'uName': uName, 'last_article': last_article,
                           'next_article': next_article, 'item_id': item_id, 'pl': pl})
    else:
        first = PTArticle.objects.first()
        last = PTArticle.objects.last()
        article = PTArticle.objects.get(id=item_id)
        article_id = PTArticle.objects.all()
        demo_id = []
        for item in article_id:
            demo_id.append(item.id)
        if str(first.id) == str(item_id):
            last_article = {'title': '到顶了，已无文章------', 'id': item_id}
        else:
            last_article = PTArticle.objects.get(id=demo_id[demo_id.index(item_id) - 1])
        if str(last.id) == str(item_id):
            next_article = {'title': '到底了，已无文章------', 'id': item_id}
        else:
            next_article = PTArticle.objects.get(id=demo_id[demo_id.index(item_id) + 1])
        pl = Comment.objects.filter(article_id=item_id).order_by('-id')
        for i in pl:
            uname = User.objects.filter(id=i.users_id).first()
            i.users_id = uname
        return render(request, "polls/PT_blog_show.html",
                      {'email': email, 'article': article, 'last_article': last_article,
                       'next_article': next_article, 'item_id': item_id, 'pl': pl})


