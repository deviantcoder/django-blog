from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
]