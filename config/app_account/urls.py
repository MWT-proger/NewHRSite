from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_request, name='ajaxLoginUrl'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.register, name='signUpUrl'),
    path('reset_password/', views.reset_password, name='resetPasswordUrl'),


    path('ajax/validate_username/', views.validate_username, name='validate_username'),
    path('ajax/validate_username_forgot/', views.validate_username_forgot_password,
         name='validateUsernameForgotPassword'),
    path('ajax/validate_email/', views.validate_email, name='validateEmailUser'),
    path('ajax/validate_authenticate/', views.validate_authenticate, name='validateAuthenticate'),
    path('ajax/call_request/', views.call_request, name='callRequest'),
    path('ajax/validate_token/', views.validate_token, name='validateToken'),

]
