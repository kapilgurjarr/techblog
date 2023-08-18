from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError



class LoginAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='Email',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    def clean(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        try:
            user=User.objects.get(email=email)
            print(user)
            if not user.is_active:
                raise self.confirm_login_allowed(user)

        except User.DoesNotExist:
            raise self.get_invalid_login_error()
        
        if email is not None and password:
            self.user_cache = authenticate(
                self.request, username=user.username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', 'password1', 'password2']


    def clean(self):
        """Form Validations"""
        cd = self.cleaned_data
        cd_email = cd.get('email')
        if User.objects.filter(email=cd_email).exists():
            raise ValidationError('Account with this email already exists.')

        return cd

    def save(self,commit=True):
        user=super().save(commit=False)
        username='@'+self.cleaned_data['email'].split('@')[0]
        user.username=username
        user.is_active=False
        if commit:
            user.save()
        return user



