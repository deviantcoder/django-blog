from django.shortcuts import render, redirect


def posts_list(request):
    return render(request, 'blog/posts-list.html')
