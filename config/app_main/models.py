from django.db import models
from django.utils.translation import gettext_lazy as _


class GeneralSettings(models.Model):
    """ Основные настройки """
    head = models.TextField(_("Вставка в head"), null=True, blank=True)
    url = models.SlugField(max_length=100, unique=True, verbose_name=_("Url страницы"), help_text='Не менять!')

    show_1 = models.BooleanField(verbose_name=_("Показывать рекламу №1"), default=True)
    advertising_1 = models.TextField(_("Реклама № 1 (Главная)"), null=True, blank=True)

    show_2 = models.BooleanField(verbose_name=_("Показывать рекламу №2"), default=True)
    advertising_2 = models.TextField(_("Реклама № 2 (Списки)"), null=True, blank=True)

    show_3 = models.BooleanField(verbose_name=_("Показывать рекламу №3"), default=True)
    advertising_3 = models.TextField(_("Реклама № 3(Личный кабинет)"), null=True, blank=True)

    show_4 = models.BooleanField(verbose_name=_("Показывать рекламу №4"), default=True)
    advertising_4 = models.TextField(_("Реклама № 4"), null=True, blank=True)

    show_5 = models.BooleanField(verbose_name=_("Показывать рекламу №5"), default=True)
    advertising_5 = models.TextField(_("Реклама № 5"), null=True, blank=True)

    show_6 = models.BooleanField(verbose_name=_("Показывать рекламу №6"), default=True)
    advertising_6 = models.TextField(_("Реклама № 6"), null=True, blank=True)

    show_7 = models.BooleanField(verbose_name=_("Показывать рекламу №7"), default=True)
    advertising_7 = models.TextField(_("Реклама № 7"), null=True, blank=True)

    show_8 = models.BooleanField(verbose_name=_("Показывать рекламу №8"), default=True)
    advertising_8 = models.TextField(_("Реклама № 8"), null=True, blank=True)

    title_main = models.CharField(_("Заголовок главной страницы"), max_length=100)
    description_main = models.TextField(_("Описание главной страницы"), null=True, blank=True)
    title_icon_1 = models.CharField(_("Заголовок плюса 1"), max_length=100)
    description_icon_1 = models.TextField(_("Описание плюса 1"), null=True, blank=True)
    title_icon_2 = models.CharField(_("Заголовок плюса 2"), max_length=100)
    description_icon_2 = models.TextField(_("Описание плюса 2"), null=True, blank=True)

    def __str__(self):
        return "Основные настройки с полем url = general. Не удалять!!!"

    class Meta:
        verbose_name = _("Основные настройки")
        verbose_name_plural = _("Основные настройки")


def get_image_name(instance, filename):
    directory = 'app_main/'
    path = directory + filename
    return path


class Image(models.Model):
    """ Изображения"""
    title = models.CharField(_("Название"), max_length=100)
    image = models.ImageField(_('Изображение'), upload_to=get_image_name,
                              help_text=_("Минимальная рекомендуемая ширина __"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Фото для слайдера")
        verbose_name_plural = _("Фотографии для слайдера")
