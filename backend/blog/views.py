from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

from .forms import UsernameUpdateForm, ProfileImageUpdateForm


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
        
        if 'update_image' in request.POST:
            form = ProfileImageUpdateForm(request.POST, request.FILES, instance=user.profile)

            if form.is_valid():
                form.save()
                messages.success(request, 'Profile picture updated')
                return redirect('blog:account_settings')
            else:
                for errors in form.errors.values():
                    for error in errors:
                        messages.warning(request, error.capitalize())

                return redirect('blog:account_settings')
    
    context = {
        'username_update_form': UsernameUpdateForm(user=user, instance=user),
        'image_update_form': ProfileImageUpdateForm(instance=user.profile)
    }

    return render(request, 'blog/account-settings.html', context)
