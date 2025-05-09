from django import forms
from django.contrib.auth import get_user_model


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
        if not username:
            raise forms.ValidationError("Username cannot be empty.")
        if self.user and username == self.user.username:
            raise forms.ValidationError("This is already your username.")
        if User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("This username is already taken.")
        return username
