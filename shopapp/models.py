import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    last_name = models.CharField(max_length=254, verbose_name="Фамилия")
    first_name = models.CharField(max_length=254, verbose_name="Имя")
    email = models.EmailField(max_length=254, verbose_name="Почта", unique=True)
    username = models.CharField(max_length=254, verbose_name="Логин", unique=True)
    password = models.CharField(max_length=254, verbose_name="Пароль")
    avatar = models.ImageField(upload_to="polls/user", verbose_name="Фото профиля")
    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
