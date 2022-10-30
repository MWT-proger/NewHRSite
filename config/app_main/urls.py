from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name="mainUrl"),
    # path('email/', views.email),
]
