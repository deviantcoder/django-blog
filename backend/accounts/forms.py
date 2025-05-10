import re

from django.forms import ValidationError
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User
from .utils import send_verification_email


class LoginForm(AuthenticationForm):
    """
    Custom form that extends Django's built-in AuthenticationForm.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter your username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter your password'})


class RegisterForm(UserCreationForm):
    """
    Custom user registration form that extends Django's UserCreationForm.
    """

    class Meta:
        model = User
        fields = (
            'email', 'username', 'password1', 'password2',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email address'})
        self.fields['username'].widget.attrs.update({'placeholder': 'Choose a username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Create a password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm your password'})

    def save(self, commit=True):
        user = super().save(commit=False)

        user.is_active = False

        if commit:
            user.save()
            send_verification_email(user)

        return user
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError('Email is already taken')
        
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError(
                'Username can only contain English letters, numbers and underscores'
            )

        if User.objects.filter(username=username).exists():
            raise ValidationError('Username is already taken')
        
        return username
