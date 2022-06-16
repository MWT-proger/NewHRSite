import json
import requests

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.http import QueryDict
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from app_main.decorators import checking_user


from .decorators import checking_profile_employer, checking_profile_applicant
from .models import TokenSignUp
from .forms import UserRegistrationForm, UserResetPasswordForm, UserUpdateForm, UserEmployerUpdateForm

User = get_user_model()

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
            print(username[0])
            username = username.replace('8', '7', 1)
        print(username)
    return username


def get_login_form_ajax(request):
    """Получение - правильной формы для авторизации пользователя из Ajax"""

    csrf = request.POST.get('csrfmiddlewaretoken', None)
    username = request.POST.get('loginNumberPhone', None)
    password = request.POST.get('loginPassword', None)

    username = edit_username(username)
    ajax_dict = {'csrfmiddlewaretoken': csrf, 'username': username, 'password': password, }
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
    username = request.POST.get('forgotPasswordNumberPhone', None)
    password = request.POST.get('forgotPasswordPassword', None)
    password2 = request.POST.get('forgotPasswordConfirmPassword', None)

    username = edit_username(username)
    ajax_dict = {'csrfmiddlewaretoken': csrf,
                 'username': username,
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
            if TokenSignUp.objects.filter(username=new_user.username,
                                          email=new_user.email,
                                          key=token).exists():
                new_user.set_password(user_form.cleaned_data['password'])
                if user_form.cleaned_data['name_company']:
                    new_user.type = 'employer'
                new_user.save()
                login(request, new_user)
                return redirect("profile")

    form = UserRegistrationForm()
    return render(request=request, template_name="app_main/index.html", context={"signup_form": form})


def reset_password(request):
    """Регистрация"""
    if request.method == 'POST':
        data = get_reset_password_form_ajax(request)
        form = UserResetPasswordForm(data)
        if form.is_valid():
            token = request.POST.get('forgotPasswordConfirmKey', None)
            if TokenSignUp.objects.filter(username=form.cleaned_data['username'], key=token).exists():
                user = User.objects.get(username=form.cleaned_data['username'])
                user.set_password(form.cleaned_data['password'])
                user.save()
                login(request, user)
                return redirect("profile")

    form = UserResetPasswordForm()
    return render(request=request, template_name="app_main/index.html", context={"reset_form": form})


@checking_user
def login_request(request):
    """Вход"""
    if request.method == "POST":
        data = get_login_form_ajax(request)
        form = AuthenticationForm(request, data=data)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("profile")
    form = AuthenticationForm()
    return render(request=request, template_name="app_main/index.html", context={"login_form": form})


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


def validate_username_forgot_password(request):
    """Проверка - существует ли пользователь с таким номером телефона"""
    username = request.GET.get('forgotPasswordNumberPhone', None)
    username = edit_username(username)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
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
        username = request.POST.get('signUpNumberPhone', None)
        if not username:
            username = request.POST.get('forgotPasswordNumberPhone', None)

        username = edit_username(username)
        params = {
            "app_id": settings.TELPHIN_APP_ID,
            "app_secret": settings.TELPHIN_APP_SECRET,
            "number": '+' + username
        }

        result = requests.post(settings.TELPHIN_URL_ONE, data=json.dumps(params), headers=HEADERS)
        response_api = result.json()

        if response_api['status'] == "success":
            status = True
            description = False
        else:
            status = False
            if response_api['description'] == 'one_call_for_two_minutes':
                description = 'Превышен лимит запросов, повторите через 2 минуты'
            elif response_api['description'] == 'ten_calls_per_day':
                description = 'На данный номер телефона превышен лимит запросов в сутки'
            else:
                description = 'Ошибка сервера, попробуйте ещё раз'
        response = {
            'is_taken': status,
            'description': description
        }
        return JsonResponse(response)


def validate_token(request):
    """Проверка кода подтверждения пользователя"""
    if request.method == "POST":
        username = request.POST.get('signUpNumberPhone', None)
        if not username:
            username = request.POST.get('forgotPasswordNumberPhone', None)
            name = edit_username(username)
            if not User.objects.filter(username__iexact=name).exists():
                response = {
                    'is_taken': False,
                    'description': "Пользователь с таким номером телефона не существует"
                }
                return JsonResponse(response)

            key = request.POST.get('forgotPasswordConfirmKey', None)
        else:
            key = request.POST.get('signUpConfirmKey', None)
        email = request.POST.get('signUpEmail', None)
        username = edit_username(username)

        params = {
            "app_id": settings.TELPHIN_APP_ID,
            "app_secret": settings.TELPHIN_APP_SECRET,
            "number": '+' + username,
            "auth_code": key
        }

        result = requests.post(settings.TELPHIN_URL_TWO, data=json.dumps(params), headers=HEADERS)
        response_api = result.json()

        if response_api['status'] == "succes":
            status = True
            description = False
            TokenSignUp.objects.create(username=username, email=email, key=key)
        else:
            status = False
            if response_api['description'] == 'code_lifetime_expired':
                description = 'Время жизни кода подтверждения истекло'
            elif response_api['description'] == 'auth_code_does_not_exist':
                description = 'Для данного номера не существует кода подтверждения'
            elif response_api['description'] == 'auth_attempts_ended':
                description = 'Закончились попытки ввода кода подтверждения'
            elif response_api['description'] == 'invalid_code':
                description = 'Не верный код подтверждения'
            else:
                description = 'Ошибка сервера, попробуйте ещё раз'
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
        form = AuthenticationForm(request, data=data)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                response = {'is_taken': True}
    return JsonResponse(response)
