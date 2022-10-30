# flake8: noqa E501
from django.conf import settings as django_settings
from django.test.signals import setting_changed
from django.utils.functional import LazyObject
from django.utils.module_loading import import_string


EMAIL_SENDER_NAMESPACE = "EMAIL_SENDER"


class ObjDict(dict):
    def __getattribute__(self, item):
        try:
            val = self[item]
            if isinstance(val, str):
                val = import_string(val)
            elif isinstance(val, (list, tuple)):
                val = [import_string(v) if isinstance(v, str) else v for v in val]
            self[item] = val
        except KeyError:
            val = super().__getattribute__(item)

        return val


default_settings = {
    "EMAIL": ObjDict(
        {
            "notification_vacancy": "email_sender.email.VacancySendEmail",
            "notification_questionnaire": "email_sender.email.QuestionnaireSendEmail",
            "forgot_password": "email_sender.email.ForgotPasswordSendEmail",
            "sign_up": "email_sender.email.SignUpSendEmail",
        })
}


class Settings:
    """
     Основные настройки приложения
    """
    def __init__(self, default_settings, explicit_overriden_settings: dict = None):
        if explicit_overriden_settings is None:
            explicit_overriden_settings = {}

        overriden_settings = (
            getattr(django_settings, EMAIL_SENDER_NAMESPACE, {})
            or explicit_overriden_settings
        )

        self._load_default_settings()
        self._override_settings(overriden_settings)

    def _load_default_settings(self):
        for setting_name, setting_value in default_settings.items():
            if setting_name.isupper():
                setattr(self, setting_name, setting_value)

    def _override_settings(self, overriden_settings: dict):
        for setting_name, setting_value in overriden_settings.items():
            value = setting_value
            if isinstance(setting_value, dict):
                value = getattr(self, setting_name, {})
                value.update(ObjDict(setting_value))
            setattr(self, setting_name, value)


class LazySettings(LazyObject):
    def _setup(self, explicit_overriden_settings=None):
        self._wrapped = Settings(default_settings, explicit_overriden_settings)


settings = LazySettings()


def reload_settings(*args, **kwargs):
    global settings
    setting, value = kwargs["setting"], kwargs["value"]
    if setting == EMAIL_SENDER_NAMESPACE:
        settings._setup(explicit_overriden_settings=value)


setting_changed.connect(reload_settings)
