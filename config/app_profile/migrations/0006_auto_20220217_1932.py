# Generated by Django 3.2.6 on 2022-02-17 16:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_profile', '0005_questionnaire_count_see'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkMode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Режим работы',
                'verbose_name_plural': 'Режимы работы',
            },
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='questionnaire', to='app_account.user', verbose_name='Соискатель'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата публикации')),
                ('status', models.CharField(choices=[('removed', 'снят'), ('active', 'активен'), ('deleted', 'удалён'), ('inspection', 'на проверке'), ('revision', 'отправлен на доработку')], default='inspection', max_length=100, verbose_name='Статус')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование вакансии')),
                ('money', models.CharField(max_length=200, verbose_name='Размер заработной платы')),
                ('accommodation', models.BooleanField(default=False, verbose_name='Проживание')),
                ('food', models.BooleanField(default=False, verbose_name='Питание')),
                ('drive', models.BooleanField(default=False, verbose_name='Проезд')),
                ('requirements', models.TextField(blank=True, null=True, verbose_name='Требования')),
                ('conditions', models.TextField(blank=True, null=True, verbose_name='Условия')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='app_profile.city', verbose_name='Город')),
                ('count_see', models.ManyToManyField(blank=True, related_name='vacancy_see', to=settings.AUTH_USER_MODEL, verbose_name='Просмотры')),
                ('profession', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app_profile.profession', verbose_name='Профессия')),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='app_profile.region', verbose_name='Регион')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancy', to=settings.AUTH_USER_MODEL, verbose_name='Работодатель')),
                ('work_mode', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_profile.workmode', verbose_name='Режим работы')),
            ],
            options={
                'verbose_name': 'Вакансия',
                'verbose_name_plural': 'Вакансии',
            },
        ),
    ]