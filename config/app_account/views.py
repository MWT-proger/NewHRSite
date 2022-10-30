import json
import logging
import random

from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.http import QueryDict
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.utils import timezone

from django.contrib.auth import login, logout
from app_main.decorators import checking_user
from email_sender.conf import settings as email_sender_settings


from .decorators import checking_profile_employer, checking_profile_applicant
from .models import TokenSignUp
from .forms import UserRegistrationForm, UserResetPasswordForm, UserUpdateForm, UserEmployerUpdateForm, \
    UsernameEmailAuthenticationForm

User = get_user_model()

logger = logging.getLogger(__name__)

HEADERS = {'Content-type': 'application/json'}


@method_decorator(login_required, name='dispatch')
@method_decorator(checking_profile_applicant, name='dispatch')
class UserUpdate(UpdateView):
    """Общие настройки пользователя"""
    model = User
    form_class = UserUpdateForm
    template_name = 'app_account/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        """Привязываем к авторизованному пользователю"""
        return self.request.user


@method_decorator(login_required, name='dispatch')
@method_decorator(checking_profile_employer, name='dispatch')
class UserEmployerUpdate(UpdateView):
    """Общие настройки пользователя - работодателя"""
    model = User
    form_class = UserEmployerUpdateForm
    template_name = 'app_account/profile.html'
    success_url = reverse_lazy('profileEmployer')

    def get_object(self):
        """Привязываем к авторизованному пользователю"""
        return self.request.user


def add_image_avatar(request):
    """Ajax функция _ отвечает за загрузку фотографии в общих настройках"""
    if request.method == 'POST':
        img = request.FILES['image']
        users = User.objects.get(username=request.user.username)
        users.image = img
        users.save()
        return HttpResponse(json.dumps({'image': str(users.image.url)}), content_type="application/json")


def logout_view(request):
    logout(request)
    return redirect("mainUrl")


def edit_username(username):
    if username:
        username = username.replace('(', '').replace(')', '').replace('-', '').replace('+', '').replace(' ', '')
        if username[0] == "8":
            username = username.replace('8', '7', 1)
    return username


def get_login_form_ajax(request):
    """Получение - правильной формы для авторизации пользователя из Ajax"""

    csrf = request.POST.get('csrfmiddlewaretoken', None)
    email = request.POST.get('loginEmail', None)
    username = request.POST.get('loginNumberPhone', None)
    password = request.POST.get('loginPassword', None)

    username = edit_username(username)
    ajax_dict = {'csrfmiddlewaretoken': csrf, 'username': username, 'password': password, 'email': email}
    query_dict = QueryDict('', mutable=True)
    query_dict.update(ajax_dict)
    return query_dict


def get_register_form_ajax(request):
    """Получение - правильной формы для регистрации пользователя из Ajax"""

    csrf = request.POST.get('csrfmiddlewaretoken', None)
    username = request.POST.get('signUpNumberPhone', None)
    name_company = request.POST.get('signUpNameCompany', None)
    email = request.POST.get('signUpEmail', None)
    password = request.POST.get('signUpPassword', None)
    password2 = request.POST.get('signUpConfirmPassword', None)

    username = edit_username(username)
    ajax_dict = {'csrfmiddlewaretoken': csrf,
                 'username': username,
                 'name_company': name_company,
                 'email': email,
                 'password': password,
                 'password2': password2,
                 }
    query_dict = QueryDict('', mutable=True)
    query_dict.update(ajax_dict)
    return query_dict


def get_reset_password_form_ajax(request):
    """Получение - правильной формы для сброса пароля пользователя из Ajax"""

    csrf = request.POST.get('csrfmiddlewaretoken', None)
    email = request.POST.get('forgotPasswordEmail', None)
    password = request.POST.get('forgotPasswordPassword', None)
    password2 = request.POST.get('forgotPasswordConfirmPassword', None)

    ajax_dict = {'csrfmiddlewaretoken': csrf,
                 'email': email,
                 'password': password,
                 'password2': password2,
                 }
    query_dict = QueryDict('', mutable=True)
    query_dict.update(ajax_dict)
    return query_dict


@checking_user
def register(request):
    """Регистрация"""
    if request.method == 'POST':
        data = get_register_form_ajax(request)
        user_form = UserRegistrationForm(data)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            token = request.POST.get('signUpConfirmKey', None)
            model = TokenSignUp.objects.filter(username=new_user.username,
                                               email=new_user.email,
                                               key=token,
                                               scene="valid")
            if model.exists():
                new_user.set_password(user_form.cleaned_data['password'])
                if user_form.cleaned_data['name_company']:
                    new_user.type = 'employer'
                new_user.save()
                model = model[0]
                model.scene = "close"
                model.save()
                login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect("profile")

    form = UserRegistrationForm()
    return render(request=request, template_name="app_main/new_index.html", context={"signup_form": form})


def reset_password(request):
    """Регистрация"""
    if request.method == 'POST':
        data = get_reset_password_form_ajax(request)
        form = UserResetPasswordForm(data)
        if form.is_valid():
            token = request.POST.get('forgotPasswordConfirmKey', None)
            model = TokenSignUp.objects.filter(email=form.cleaned_data['email'], key=token, scene="valid")
            if model.exists():
                user = User.objects.get(email=form.cleaned_data['email'])
                user.set_password(form.cleaned_data['password'])
                user.save()
                model = model[0]
                model.scene = "close"
                model.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect("profile")

    form = UserResetPasswordForm()
    return render(request=request, template_name="app_main/new_index.html", context={"reset_form": form})


@checking_user
def login_request(request):
    """Вход"""
    if request.method == "POST":
        data = get_login_form_ajax(request)
        form = UsernameEmailAuthenticationForm(request, data=data)
        if form.is_valid():
            user = form.get_user()

            if user is not None:
                login(request, user)
                return redirect("profile")

    form = UsernameEmailAuthenticationForm()
    return render(request=request, template_name="app_main/new_index.html", context={"login_form": form})


@login_required
def profile(request):
    return render(request, 'app_account/profile.html')


def validate_username(request):
    """Проверка - доступен ли номер телефона для регистрации"""
    username = request.GET.get('signUpNumberPhone', None)
    username = edit_username(username)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)


def validate_email_forgot_password(request):
    """Проверка - существует ли пользователь с таким email"""
    email = request.GET.get('forgotPasswordEmail', None)
    response = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    logger.debug('validate_email_forgot_password', response)
    return JsonResponse(response)


def validate_email(request):
    """Проверка -  доступна ли электронная почта для регистрации"""
    email = request.GET.get('signUpEmail', None)
    response = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(response)


def call_request(request):
    """Запрос на осуществления звонка пользователю для подтверждения регистрации или сброса пароля"""
    if request.method == "POST":
        error = False
        forgot = False
        email = request.POST.get('signUpEmail', None)
        if not email:
            email = request.POST.get('forgotPasswordEmail', None)
            forgot = True

            if not User.objects.filter(email__iexact=email).exists():
                error = True
                status = False
                description = 'Пользователь с таким адресом электронной почты не существует'

        logger.debug("call_request: %s", email)

        if not error:
            key = str(random.randint(1111, 9999))
            context = {'validate_code': key}

            TokenSignUp.objects.create(email=email, key=key)
            status = True
            description = False

            if forgot:
                email_sender_settings.EMAIL.forgot_password(context).send([email])
            else:
                email_sender_settings.EMAIL.sign_up(context).send([email])

        response = {
            'is_taken': status,
            'description': description
        }
        return JsonResponse(response)


def validate_token(request):
    """Проверка кода подтверждения пользователя"""
    if request.method == "POST":
        email = request.POST.get('signUpEmail', None)

        if not email:
            email = request.POST.get('forgotPasswordEmail', None)

            if not User.objects.filter(email__iexact=email).exists():
                response = {
                    'is_taken': False,
                    'description': "Пользователь с таким адресом электронной почты не существует"
                }
                return JsonResponse(response)

            key = request.POST.get('forgotPasswordConfirmKey', None)
        else:
            key = request.POST.get('signUpConfirmKey', None)

        username = request.POST.get('signUpNumberPhone', None)
        username = edit_username(username)
        model = TokenSignUp.objects.filter(email=email, key=key, scene="create")
        if model.exists():

            limit = timezone.now() - timedelta(minutes=5)
            model = model[0]
            if model.created_at < limit:
                status = False
                description = 'Время жизни кода подтверждения истекло'
            else:
                status = True
                description = False
                model.username = username
                model.scene = "valid"
                model.save()
        else:
            status = False
            description = 'Не верный код подтверждения'

        response = {
            'is_taken': status,
            'description': description
        }
        return JsonResponse(response)


def validate_authenticate(request):
    """Проверка - правильно ли указаны логин и пароль"""
    response = {'is_taken': False}
    if request.method == "POST":
        data = get_login_form_ajax(request)
        logger.info(data)
        form = UsernameEmailAuthenticationForm(request, data=data)
        logger.info(form.is_valid())
        if form.is_valid():
            user = form.get_user()

            if user is not None:
                response = {'is_taken': True}

    return JsonResponse(response)
