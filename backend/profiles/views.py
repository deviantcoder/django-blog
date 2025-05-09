from django.shortcuts import render

from .forms import ProfileForm


def edit_profile(request):
    context = {
        'form': ProfileForm(),
    }

    return render(request, 'profiles/edit_profile.html', context)
