from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import Questionnaire, Vacancy


def checking_my_questionnaire(f):
    """Проверяем на наличие уже созданной модели и наша ли она, если нет то выдаём ошибку"""
    def wrap(request, *args, **kwargs):
        model = Questionnaire.objects.filter(slug=kwargs['slug'], user=request.user)

        if model.exists():
            if model[0].status == 'deleted':
                return HttpResponseRedirect(reverse('my_questionnaire_list'))
        else:
            return HttpResponseRedirect(reverse('questionnaire_detail', kwargs={'slug': kwargs['slug']}))
        return f(request, *args, **kwargs)
    return wrap


def checking_my_questionnaire_edit(f):
    """Проверяем на наличие уже созданной модели и наша ли она, если нет то выдаём ошибку"""
    def wrap(request, *args, **kwargs):
        model = Questionnaire.objects.filter(slug=kwargs['slug'], user=request.user).exclude(status='active')
        if model.exists():
            if model[0].status == 'deleted':
                return HttpResponseRedirect(reverse('my_questionnaire'))
        else:
            return HttpResponseRedirect(reverse('my_questionnaire_detail', kwargs={'slug': kwargs['slug']}))
        return f(request, *args, **kwargs)
    return wrap


def checking_min_one_questionnaire(f):
    """Проверяет существует ли у пользователя хотя бы одна анкета если нет отправляет заполнить"""
    def wrap(request, *args, **kwargs):
        model = Questionnaire.objects.filter(user=request.user)
        if not model.exists():
            messages.info(request, 'Для просмотра списка вакансий необходимо добавить минимум одну анкету.')
            return HttpResponseRedirect(reverse('questionnaire_create'))
        return f(request, *args, **kwargs)
    return wrap


def checking_my_limit_questionnaire(f):
    """Проверяем на наличие уже предельного колличества анкет"""
    def wrap(request, *args, **kwargs):
        model = Questionnaire.objects.filter(user=request.user).exclude(status='deleted')
        if model.count() > 4:
            messages.info(request, 'Вы добавили  максимальное колличество анкет. '
                                   'Для создание новой вам необходимо удалить одну из созданных!')
            return HttpResponseRedirect(reverse('my_questionnaire_list'))
        return f(request, *args, **kwargs)
    return wrap


def checking_my_vacancy(f):
    """Проверяем на наличие уже созданной модели и наша ли она, если нет то выдаём ошибку"""
    def wrap(request, *args, **kwargs):
        model = Vacancy.objects.filter(slug=kwargs['slug'], user=request.user)

        if model.exists():
            if model[0].status == 'deleted':
                return HttpResponseRedirect(reverse('my_vacancy_list'))
        else:
            return HttpResponseRedirect(reverse('vacancy_detail', kwargs={'slug': kwargs['slug']}))
        return f(request, *args, **kwargs)
    return wrap


def checking_my_vacancy_edit(f):
    """Проверяем на наличие уже созданной модели и наша ли она, если нет то выдаём ошибку"""
    def wrap(request, *args, **kwargs):
        model = Vacancy.objects.filter(slug=kwargs['slug'], user=request.user).exclude(status='active')

        if model.exists():
            if model[0].status == 'deleted':
                return HttpResponseRedirect(reverse('my_vacancy'))
        else:
            return HttpResponseRedirect(reverse('my_vacancy_detail', kwargs={'slug': kwargs['slug']}))
        return f(request, *args, **kwargs)
    return wrap
