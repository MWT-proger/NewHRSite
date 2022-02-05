from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.http import QueryDict
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

User = get_user_model()


def get_login_form_ajax(request):
    """Получение - правильной формы для авторизации пользователя из Ajax"""
    
    csrf = request.POST.get('csrfmiddlewaretoken', None)
    username = request.POST.get('loginNumberPhone', None)
    password = request.POST.get('loginPassword', None)

    if username:
        username = username.replace('(', '-').replace(')', '-')
    ajax_dict = {'csrfmiddlewaretoken': csrf, 'username': username, 'password': password, }
    query_dict = QueryDict('', mutable=True)
    query_dict.update(ajax_dict)
    return query_dict


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
    if username:
        username = username.replace('(', '-').replace(')', '-')
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)


def validate_username_forgot_password(request):
    """Проверка - существует ли пользователь с таким номером телефона"""
    username = request.GET.get('forgotPasswordNumberPhone', None)
    if username:
        username = username.replace('(', '-').replace(')', '-')
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
