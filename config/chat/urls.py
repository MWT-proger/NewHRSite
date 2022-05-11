# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('<str:username>', views.DialogListView.as_view(), name='dialogs_detail'),
    path('', views.DialogListView.as_view(), name='dialogs'),

]

