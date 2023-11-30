from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class CustomUserLoginForm(AuthenticationForm):
    email = forms.EmailField(max_length=254, help_text='', widget=forms.EmailInput(attrs={'autofocus': True}))

    def __init__(self, request=None, *args, **kwargs):
        super(CustomUserLoginForm, self).__init__(request, *args, **kwargs)

        self.fields['email'] = self.fields['username']
        del self.fields['username']
