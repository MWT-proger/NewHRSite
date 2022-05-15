import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

User = get_user_model()

STATUS = [
    ('removed', 'снят'),
    ('active', 'активен'),
    ('deleted', 'удалён'),
    ('inspection', 'на проверке'),
    ('revision', 'отправлен на доработку')
]


class Region(models.Model):
    """Регион"""
    name = models.CharField("Название", max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"


class City(models.Model):
    """Город"""
    name = models.CharField("Название", max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"


class Profession(models.Model):
    """Профессия"""
    name = models.CharField("Название", max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Профессия"
        verbose_name_plural = "Профессии"


class WorkMode(models.Model):
    """Режим работы"""
    name = models.CharField("Название", max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Режим работы"
        verbose_name_plural = "Режимы работы"


class DriverLicense(models.Model):
    """Водительское удостоверение"""
    name = models.CharField("Название", max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Водительское удостоверение"
        verbose_name_plural = "Водительские удостоверения"


class Questionnaire(models.Model):
    """Анкета соискателя"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="questionnaire",
                             verbose_name="Соискатель")
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    public_date = models.DateTimeField(verbose_name="Дата публикации", default=timezone.now)
    status = models.CharField('Статус', max_length=100, default='inspection', choices=STATUS)
    # Информация Которую все видят
    region = models.ForeignKey(Region, verbose_name="Регион проживания", on_delete=models.PROTECT, null=True)
    city = models.ForeignKey(City, verbose_name="Город проживания (для деревнь и поселков указать районный центр)", on_delete=models.PROTECT, null=True)

    phone = models.CharField("Номер телефона", max_length=30)
    health_book = models.BooleanField(verbose_name="Санитарная книжка", default=False)
    vaccinated = models.BooleanField(verbose_name="Наличие прививки от коронавируса", default=False)
    no_profession = models.BooleanField(verbose_name="Нет профессии", default=False)
    not_citizen = models.BooleanField(verbose_name="Не являюсь гражданином РФ", default=False)
    profession = models.ForeignKey(Profession, verbose_name="Профессия (Профильное образование)",
                                   on_delete=models.PROTECT, null=True, blank=True)
    driver_license = models.ManyToManyField(DriverLicense, verbose_name="Водительское удостоверение", blank=True,
                                            related_name="questionnaire", help_text='выберите все открытые категории')
    total_service = models.PositiveIntegerField("Общий трудовой стаж", default=0)
    driving_experience = models.PositiveIntegerField("Водительский стаж", default=0)
    self_propelled = models.BooleanField(verbose_name="Права на  управление самоходными машинами", default=False,
                                         help_text='просьба оставить комментарий в поле "Дополнительная информация"')
    description = models.TextField("Дополнительная информация", null=True, blank=True,
                                   help_text='кратко изложите ваши ключевые навыки, опыт работы, '
                                             'законченные курсы если таковые имеются')

    count_see = models.ManyToManyField(User,
                                       verbose_name="Просмотры", blank=True,
                                       related_name="questionnaire_see")

    count_sentence = models.ManyToManyField(User,
                                            verbose_name="Предложения", blank=True,
                                            related_name="questionnaire_sentence")

    def get_admin_url(self):
        return reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name), args=(self.id,))

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("my_questionnaire_detail", kwargs={'slug': self.slug})

    def get_edit_url(self):
        return reverse("questionnaire_edit", kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse("questionnaire_delete", kwargs={'slug': self.slug})

    def get_absolute_other_url(self):
        return reverse("questionnaire_detail", kwargs={'slug': self.slug})

    def get_chat_url(self):
        return reverse("dialogs_detail", kwargs={'username': self.user.username})

    class Meta:
        verbose_name = "Анкета соискателя"
        verbose_name_plural = "Анкеты соискателей"


class Vacancy(models.Model):
    """Вакансии"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vacancy",
                             verbose_name="Работодатель")
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    public_date = models.DateTimeField(verbose_name="Дата публикации", default=timezone.now)
    status = models.CharField('Статус', max_length=100, default='active', choices=STATUS)
    # Информация Которую все видят

    name = models.CharField('Наименование вакансии', max_length=200)
    region = models.ForeignKey(Region, verbose_name="Регион", on_delete=models.PROTECT, null=True)
    city = models.ForeignKey(City, verbose_name="Город (для деревнь и поселков указать районный центр)", on_delete=models.PROTECT, null=True)
    profession = models.ForeignKey(Profession, verbose_name="Профессия", on_delete=models.PROTECT, null=True,
                                   blank=True)
    work_mode = models.ForeignKey(WorkMode, verbose_name="Режим работы", on_delete=models.PROTECT)
    money = models.PositiveIntegerField("Размер заработной платы", default=0, help_text='В рублях')

    accommodation = models.BooleanField(verbose_name="Проживание", default=False)
    food = models.BooleanField(verbose_name="Питание", default=False)
    drive = models.BooleanField(verbose_name="Проезд", default=False)

    requirements = models.TextField("Требования", null=True, blank=True)
    conditions = models.TextField("Условия", null=True, blank=True)

    count_see = models.ManyToManyField(User,
                                       verbose_name="Просмотры", blank=True,
                                       related_name="vacancy_see")
    count_sentence = models.ManyToManyField(User,
                                            verbose_name="Предложения", blank=True,
                                            related_name="vacancy_sentence")
    def get_admin_url(self):
        return reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name), args=(self.id,))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("my_vacancy_detail", kwargs={'slug': self.slug})

    def get_absolute_other_url(self):
        return reverse("vacancy_detail", kwargs={'slug': self.slug})

    def get_edit_url(self):
        return reverse("vacancy_edit", kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse("vacancy_delete", kwargs={'slug': self.slug})

    def get_chat_url(self):
        return reverse("dialogs_detail", kwargs={'username': self.user.username})

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
