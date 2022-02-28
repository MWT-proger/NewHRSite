from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Region, City, Profession, DriverLicense, Questionnaire, WorkMode, Vacancy


@admin.register(Region)
class RegionAdmin(ImportExportModelAdmin):
    pass


@admin.register(City)
class CityAdmin(ImportExportModelAdmin):
    pass


@admin.register(Profession)
class ProfessionAdmin(ImportExportModelAdmin):
    pass


@admin.register(DriverLicense)
class DriverLicenseAdmin(admin.ModelAdmin):
    pass


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkMode)
class WorkModeAdmin(admin.ModelAdmin):
    pass


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    pass
