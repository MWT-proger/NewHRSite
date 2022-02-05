from django.contrib.auth.models import AbstractUser
from django.db import models

TYPE = [
    ('applicant', 'Соискатель'),
    ('employer', 'Работодатель')
]


class User(AbstractUser):
    name_company = models.CharField('Название компании', max_length=200, blank=True, null=True)
    type = models.CharField('Тип пользователя', max_length=20, default='applicant', choices=TYPE)


class TokenSignUp(models.Model):
    """ Токен регистрации """
    username = models.CharField("Номер телефона", max_length=20)
    email = models.EmailField("Адрес электронной почты", blank=True, null=True)
    key = models.CharField("Сам ключ", max_length=4)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Токен регистрации"
        verbose_name_plural = "Токены регистрации"
