from django import forms
from django.contrib.auth import get_user_model

from profiles.models import Profile


User = get_user_model()


class UsernameUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter a new username',
                }
            )
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']

        if not username or len(username) < 5:
            raise forms.ValidationError("Username is too short.")
        
        if len(username) > 15:
            raise forms.ValidationError('Username cannot exceed 15 characters.')
        
        if self.user and username == self.user.username:
            raise forms.ValidationError("This is already your username.")
        
        if User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("This username is already taken.")
        
        return username


class ProfileImageUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)
        widgets = {
            'image': forms.FileInput(
                attrs={
                    'name': 'image',
                    'class': 'd-none',
                    'id': 'imageInput',
                    'accept': 'image/*',
                }
            )
        }
