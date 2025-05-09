from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def posts_list(request):
    return render(request, 'blog/posts-list.html')


@login_required(login_url='accounts:login')
def account_settings(request):
    return render(request, 'blog/account-settings.html')
