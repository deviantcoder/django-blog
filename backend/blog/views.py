from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

from .forms import UsernameUpdateForm


User = get_user_model()


def posts_list(request):
    return render(request, 'blog/posts-list.html')


@login_required(login_url='accounts:login')
def account_settings(request):
    user = request.user

    if request.method == 'POST':
        if 'update_username' in request.POST:
            form = UsernameUpdateForm(request.POST, user=user, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Username changed')
                return redirect('blog:account_settings')
            else:
                for errors in form.errors.values():
                    for error in errors:
                        messages.warning(request, error.capitalize())
                return render(request, 'blog/account-settings.html', {'username_update_form': form})
    
    context = {
        'username_update_form': UsernameUpdateForm(user=user, instance=user),
    }

    return render(request, 'blog/account-settings.html', context)
