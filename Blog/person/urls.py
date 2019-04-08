from django.urls import path
from . import views
app_name = 'person'
urlpatterns = [
    path('', views.index, name='index'),
    path('pim/', views.pim, name='pim'),
    path('addArticle/', views.addArticle, name='addArticle'),
    path('myArticle/', views.myArticle, name='myArticle'),
    path('showArticle/<int:item_id>', views.showArticle, name='showArticle'),
    path('manageArticle', views.manageArticle, name='manageArticle'),

]