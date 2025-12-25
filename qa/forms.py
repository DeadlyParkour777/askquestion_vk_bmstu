from django import forms
from django.contrib.auth.models import User
from qa.models import Profile
from django.contrib.auth import authenticate
from qa.models import Question, Tag, Answer

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

        if password and password_repeat and password != password_repeat:
            raise forms.ValidationError('Пароли не совпадают')
        return cleaned_data
    
    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )

        profile = Profile.objects.create(user=user)
        if self.cleaned_data.get('avatar'):
            profile.avatar = self.cleaned_data['avatar']
            profile.save()

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

class AnswerForm(forms.Form):
    text = forms.CharField(required=True, label="Ваш ответ", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    def save(self, user, question):
        answer = Answer.objects.create(
            text=self.cleaned_data['text'],
            author=user.profile,
            question=question
        )
        return answer

class AskForm(forms.Form):
    title = forms.CharField(
        max_length=255, required=True, label="Заголовок вопроса",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    text = forms.CharField(
        required=True, label="Текст вопроса",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8})
    )

    tags = forms.CharField(
        required=True, label="Теги",
        help_text="Введите теги через запятую, не более 3-х",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'python, django, mysql'
        })
    )
    def clean_tags(self):
        tags_str = self.cleaned_data.get('tags')
        tags = [tag.strip().lower() for tag in tags_str.split(',') if tag.strip()]
        
        if len(tags) > 3:
            raise forms.ValidationError('Можно указать не более трех тегов.')
        
        for tag_name in tags:
            if not all(c.isalnum() or c == '-' for c in tag_name):
                 raise forms.ValidationError(f'Тег "{tag_name}" содержит недопустимые символы.')

        return tags

    def save(self, author):
        question = Question.objects.create(
            title=self.cleaned_data['title'],
            text=self.cleaned_data['text'],
            author=author
        )

        tag_objects = []
        for tag_name in self.cleaned_data['tags']:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_objects.append(tag)
        
        question.tags.set(tag_objects)
        
        return question

class SettingsForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, label="Логин", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(required=False, label="Аватар", widget=forms.FileInput(attrs={'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_username(self):
        username = self.cleaned_data['username']
        # Разрешаем оставить свой же ник, но запрещаем занимать чужой
        if User.objects.filter(username=username).exclude(id=self.user.id).exists():
            raise forms.ValidationError('Этот логин уже занят')
        return username

    def save(self):
        self.user.username = self.cleaned_data['username']
        self.user.email = self.cleaned_data['email']
        self.user.save()
        
        profile = self.user.profile
        if self.cleaned_data.get('avatar'):
            profile.avatar = self.cleaned_data['avatar']
            profile.save()
        return self.user
