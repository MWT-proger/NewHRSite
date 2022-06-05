from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext, gettext_lazy as _

from import_export.admin import ExportActionMixin

from .models import TokenSignUp

User = get_user_model()


@admin.register(User)
class UserAdmin(ExportActionMixin, auth_admin.UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'type', 'image')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'third_name',  'age',
                                         'email', 'name_company')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(TokenSignUp)
class TokenSignUpAdmin(admin.ModelAdmin):
    pass
