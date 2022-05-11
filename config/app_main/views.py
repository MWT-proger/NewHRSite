from django.shortcuts import render


def main(request):
    return render(request, 'app_main/new_index.html')


# def new_main(request):
#     return render(request, 'app_main/new_index.html')
