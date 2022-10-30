from django.shortcuts import render
from app_main.decorators import checking_user


@checking_user
def main(request):
    return render(request, 'app_main/new_index.html')


# def email(request):
#     return render(request, 'email_sender/email/email_forgot_password.html')
