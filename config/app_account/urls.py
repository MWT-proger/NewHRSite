from django.urls import path
from .views import home, SignUpView, validate_username, validate_email, validate_username_forgot_password

urlpatterns = [
    path('profile/', home, name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('ajax/validate_username/', validate_username, name='validate_username'),
    path('ajax/validate_username_forgot/', validate_username_forgot_password, name='validateUsernameForgotPassword'),
    path('ajax/validate_email/', validate_email, name='validateEmailUser')
]