from django.urls import reverse

from django.http import HttpResponseRedirect


def checking_profile_employer(f):
    """Определяем является ли пользователь Работодателем"""
    def wrap(request, *args, **kwargs):
        if request.user.type != 'employer' and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('profile'))
        return f(request, *args, **kwargs)
    return wrap


def checking_profile_applicant(f):
    """Определяем является ли пользователь Соискателем"""
    def wrap(request, *args, **kwargs):
        if request.user.type != 'applicant' and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('profileEmployer'))
        return f(request, *args, **kwargs)
    return wrap
