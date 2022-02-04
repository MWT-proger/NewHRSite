from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, get_user_model
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

User = get_user_model()


@login_required
def home(request):
    return render(request, 'app_account/home.html')


class SignUpView(CreateView):
    template_name = 'signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid


def validate_username(request):
    """Проверка доступности номера телефона для регистрации"""
    username = request.GET.get('signUpNumberPhone', None)
    if username:
        username = username.replace('(', '-').replace(')', '-')
    print(username.replace('(', '-').replace(')', '-'))
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)


def validate_username_forgot_password(request):
    """Проверка доступности номера телефона для регистрации"""
    username = request.GET.get('forgotPasswordNumberPhone', None)
    if username:
        username = username.replace('(', '-').replace(')', '-')
    print(username)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)


def validate_email(request):
    """Проверка доступности электронной почты для регистрации"""
    email = request.GET.get('signUpEmail', None)
    print(email)
    response = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    print(User.objects.filter(email__iexact=email).exists())
    return JsonResponse(response)
