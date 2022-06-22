import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image, ImageOps
from django.urls import reverse

TYPE = [
    ('applicant', 'Соискатель'),
    ('employer', 'Работодатель')
]

SCENE = [
    ('create', 'Создан'),
    ('valid', 'Проверен'),
    ('close', 'Закрыт')
]
_MAX_SIZE = 200


def get_image_name(instance, filename):
    """Функция установки сохранения пути для изображения пользователя"""
    directory = 'app_account/users/'
    username = '%s' % instance.username
    format = '_avatar.png'
    path = directory + username + format
    return path


class User(AbstractUser):
    image = models.ImageField('Аватарка', upload_to=get_image_name, blank=True, null=True)
    name_company = models.CharField('Название компании', max_length=200, blank=True, null=True)
    third_name = models.CharField('Отчество', max_length=200, blank=True, null=True)
    type = models.CharField('Тип пользователя', max_length=20, default='applicant', choices=TYPE)
    age = models.PositiveIntegerField("Полных лет", blank=True, null=True, default=0)

    def save(self, *args, **kwargs):
        # обычное сохранение
        super(User, self).save(*args, **kwargs)

        # Проверяем, указано ли фото пользователя

        # Проверяем, указано ли изображение
        if self.image:
            filepath = self.image.path
            width = self.image.width
            height = self.image.height
            if width > height or width == height:
                height = round((2 * width) / 3)
            else:
                width = round((3 * height) / 2)
            base_width = 300
            ratio = (base_width / float(width))
            height = int((float(height) * float(ratio)))
            image = Image.open(filepath)
            image = ImageOps.exif_transpose(image)
            image = image.resize((base_width, height), Image.ANTIALIAS)
            dirname, fname = os.path.split(filepath)
            image.save(filepath)

    def get_admin_url(self):
        return reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name), args=(self.id,))


class TokenSignUp(models.Model):
    """ Токен регистрации """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField("Номер телефона", max_length=20)
    email = models.EmailField("Адрес электронной почты", blank=True, null=True)
    key = models.CharField("Сам ключ", max_length=4)
    scene = models.CharField('Этап валидации токена', max_length=20, default='create', choices=SCENE)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Токен регистрации"
        verbose_name_plural = "Токены регистрации"
