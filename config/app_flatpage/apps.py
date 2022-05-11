from django.apps import AppConfig


class AppFlatpageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_flatpage'
    verbose_name = "Страницы правил, условий и т.д."
