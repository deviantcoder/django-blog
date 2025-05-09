from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .forms import LoginForm, RegisterForm
from .models import User


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                messages.success(request, 'Signed In')
                return redirect('/')
        else:
            if '__all__' in form.errors:
                messages.warning(request, f'Invalid username or password')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.warning(request, f'{field.capitalize()}: {error}')
            return render(request, 'accounts/login.html', {'form': form})
    else:
        form = LoginForm()

    context = {
        'form': form,
    }

    return render(request, 'accounts/login.html', context)


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'Signed Out')
    return redirect('accounts:login')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('accounts:login')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'emails/verification_sent.html')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.warning(request, f'{field.capitalize()}: {error}')
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = RegisterForm()

    context = {
        'form': form,
    }
    
    return render(request, 'accounts/register.html', context)


def verify_email(request, uidb64, token):
    if request.user.is_authenticated and request.user.email_verified:
        return redirect('/')
    
    user = None
    token_generator = PasswordResetTokenGenerator()

    try:
        uid_bytes = urlsafe_base64_decode(force_str(uidb64))
        uid_str = uid_bytes.decode('utf-8')

        user = User.objects.get(pk=uid_str)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, UnicodeDecodeError):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        if hasattr(user, 'email_verified'):
            user.email_verified = True

        user.save()

        user.backend = 'django.contrib.auth.backends.ModelBackend'

        login(request, user)
        messages.success(request, 'Signed Up')
        return redirect('/')
    elif user and not user.email_verified:
        user.delete()

    return render(request, 'emails/verification_failed.html')

