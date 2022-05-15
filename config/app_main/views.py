from django.shortcuts import render
from app_main.decorators import checking_user


@checking_user
def main(request):
    return render(request, 'app_main/new_index.html')


# def new_main(request):
#     return render(request, 'app_main/new_index.html')
