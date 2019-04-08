from django.urls import path
from . import views
app_name = 'verify'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('secede/', views.secede, name='secede')
    # path('cookie/', views.cookie)
]