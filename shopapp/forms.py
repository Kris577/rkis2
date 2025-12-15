from django import forms
from django.core.exceptions import ValidationError
from django import forms
from .models import Post, Comment, CustomUser
from django.forms.models import inlineformset_factory

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput)

    def save(self, commit=True):
        new_user = super().save(commit=False)
        new_user.set_password(self.cleaned_data.get("password"))
        if commit:
            new_user.save()
        return new_user

    def clean(self):
        super().clean()
        pwd1 = self.cleaned_data.get("password")
        pwd2 = self.cleaned_data.get("password2")
        if pwd1 and pwd2 and pwd1 != pwd2:
            raise ValidationError({"password2": ValidationError("Пароли должны совпадать", code="password_mismatch")})

    class Meta:
        model = CustomUser
        fields = ("avatar", "first_name", "last_name", "username", "email")

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))

class UpdateForm(forms.ModelForm):
    avatar = forms.ImageField(label="Фото профиля", required=False)
    last_name = forms.CharField(label="Фамилия", required=False)
    first_name = forms.CharField(label="Имя", required=False)
    email = forms.CharField(label="Почта", required=False)
    username = forms.CharField(label="Логин", required=False)

    class Meta:
        model = CustomUser
        fields = ("avatar", "last_name","first_name", "email","username")

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите текст поста', 'rows': 4}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Напишите комментарий', 'rows': 3}),
        }