from django.shortcuts import render, redirect

from .forms import LoginForm, RegisterForm


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')


def logout_user(request):
    pass


def register_user(request):
    if request.user.is_authenticated:
        return redirect('/')


def verify_email(request):
    if request.user.is_authenticated and request.user.email_verified:
        return redirect('/')
