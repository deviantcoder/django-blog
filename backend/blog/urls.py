from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.posts_list, name='posts_list'),
    path('settings/', views.account_settings, name='account_settings'),
]