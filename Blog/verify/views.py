from django.shortcuts import render, HttpResponse, redirect, reverse
from .form import RegisterForm, LoginForm
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'verify/login.html', {'form': form})
    else:
        form = LoginForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            email = form.cleaned_data['email']
            request.session['email'] = email
            return redirect(reverse("blogs:index"))
        else:
            return render(request, 'verify/login.html', {'form': form})


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'verify/register.html', {'form': form})
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.is_active = False
            form.save()
            return redirect(reverse('verify:login'))
        else:
            return render(request, 'verify/register.html', {'form': form})


def secede(request):
    if request.method == 'GET':
        del request.session['email']
        return redirect(reverse("blogs:index"))

# def cookie(request):
#     import datetime
#     # co = request.COOKIES.get('csrftoken', None)   #获取cookie
#     # print(co)
#     res = HttpResponse("123")
#     res.set_cookie('sdl', '123456789', expires=datetime.datetime(2019, 1, 1))   # 设置cookie
#     return res