from django import forms
from django.contrib.auth.models import User
from qa.models import Profile
from django.contrib.auth import authenticate

class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=100, required=True, label="Логин",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True, label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        required=True, label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password_repeat = forms.CharField(
        required=True, label="Повторите пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')

        if password and password_repeat and password_repeat != password_repeat:
            raise forms.ValidationError('Пароли не совпадают')
        return cleaned_data
    
    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )

        Profile.objects.create(user=user)
        return user

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100, required=True, label="Логин",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        required=True, label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    user_cache = None

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Неверный логин или пароль')

        return cleaned_data
    
    def get_user(self):
        return self.user_cache


