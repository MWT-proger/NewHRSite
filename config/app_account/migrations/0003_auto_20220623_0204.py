# Generated by Django 3.2.6 on 2022-06-22 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_account', '0002_alter_user_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='tokensignup',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default="2021-06-16 20:14:09.229921+00"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tokensignup',
            name='scene',
            field=models.CharField(choices=[('create', 'Создан'), ('valid', 'Проверен'), ('close', 'Закрыт')], default='create', max_length=20, verbose_name='Этап валидации токена'),
        ),
        migrations.AddField(
            model_name='tokensignup',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]