from django.urls import path
from . import views
app_name = 'blogs'
urlpatterns = [
    path('', views.index, name='index'),
    path('PT_blog_show/<int:item_id>', views.PT_blog_show, name='PT_blog_show'),
    path('getKeyword/', views.getKeyword, name='getKeyword'),
    path('my_blog/', views.my_blog, name='my_blog'),
    path('blog_show/<int:item_id>', views.blog_show, name='blog_show'),
    path('kaitong/', views.kaitong, name='kaitong')
]