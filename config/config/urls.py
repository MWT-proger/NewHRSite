from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("app_account.urls")),
    path('profile/', include("app_profile.urls")),
    path('', include("app_main.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('info/', include('django.contrib.flatpages.urls')),
    path('dialogs/', include('chat.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "VAHTOWEEK"
admin.site.index_title = "Панель администратора"
admin.site.site_title = "VAHTOWEEK"