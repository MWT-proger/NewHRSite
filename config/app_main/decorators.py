from django.urls import reverse
from django.http import HttpResponseRedirect


def checking_user(f):
    """Проверяем авторизован ли пользователь"""
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('profile'))
        return f(request, *args, **kwargs)
    return wrap
