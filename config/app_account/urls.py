from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('profile/applicant/', views.UserUpdate.as_view(), name='profile'),
    path('profile/employer/', views.UserEmployerUpdate.as_view(), name='profileEmployer'),


    path('login/', views.login_request, name='ajaxLoginUrl'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.register, name='signUpUrl'),
    path('reset_password/', views.reset_password, name='resetPasswordUrl'),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='app_account/change-password.html',
            success_url='/profile/applicant/'
        ),
        name='change_password'
    ),

    path('ajax/validate_username/', views.validate_username, name='validate_username'),
    path('ajax/validate_email_forgot/', views.validate_email_forgot_password,
         name='validateEmailForgotPasswordUser'),
    path('ajax/validate_email/', views.validate_email, name='validateEmailUser'),
    path('ajax/validate_authenticate/', views.validate_authenticate, name='validateAuthenticate'),
    path('ajax/call_request/', views.call_request, name='callRequest'),
    path('ajax/validate_token/', views.validate_token, name='validateToken'),

    path('ajax/add_image/', views.add_image_avatar, name="add_image"),
]
