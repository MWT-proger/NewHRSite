from django.contrib import admin
from django.contrib.auth.models import Group as BaseGroup

from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from import_export import resources
from import_export.fields import Field


from .models import Region, City, Profession, DriverLicense, Questionnaire, WorkMode, Vacancy

admin.site.unregister(BaseGroup)


@admin.register(Region)
class RegionAdmin(ImportExportModelAdmin):
    search_fields = (
        "name",
    )


@admin.register(City)
class CityAdmin(ImportExportModelAdmin):
    search_fields = (
        "name",
    )


@admin.register(Profession)
class ProfessionAdmin(ImportExportModelAdmin):
    search_fields = (
        "name",
    )


@admin.register(DriverLicense)
class DriverLicenseAdmin(ImportExportModelAdmin):
    search_fields = (
        "name",
    )


@admin.register(WorkMode)
class WorkModeAdmin(ImportExportModelAdmin):
    search_fields = (
        "name",
    )


class VacancyResource(resources.ModelResource):
    full_see = Field()
    full_sentence = Field()

    def dehydrate_full_see(self, obj):
        return obj.count_see.all().count()

    def dehydrate_full_sentence(self, obj):
        return obj.count_sentence.all().count()
    class Meta:
        model = Vacancy

        fields = ("id", "name", "status", "user__username", "money", "public_date", "slug", "region__name", "city__name", "profession__name",
                  "work_mode__name", "accommodation", "food", "drive", "requirements", "conditions", "full_see", "full_sentence")
        export_order = ("id", "name", "status", "user__username", "money", "public_date", "slug", "region__name", "city__name", "profession__name",
                  "work_mode__name", "accommodation", "food", "drive", "requirements", "conditions", "full_see", "full_sentence")


class QuestionnaireResource(resources.ModelResource):
    full_see = Field()
    full_sentence = Field()

    def dehydrate_full_see(self, obj):
        return obj.count_see.all().count()

    def dehydrate_full_sentence(self, obj):
        return obj.count_sentence.all().count()
    class Meta:
        model = Questionnaire

        fields = ("id", "status", "user__username",  "phone", "public_date", "slug", "region__name", "city__name",
                  "profession__name", "health_book", "vaccinated", "no_profession", "not_citizen",
                  "driver_license__name", "total_service", "driving_experience", "self_propelled", "description",
                  "full_see", "full_sentence")
        export_order = ("id", "status", "user__username",  "phone", "public_date", "slug", "region__name", "city__name",
                        "profession__name", "health_book", "vaccinated", "no_profession", "not_citizen",
                        "driver_license__name", "total_service", "driving_experience", "self_propelled", "description",
                        "full_see", "full_sentence")


@admin.register(Vacancy)
class VacancyAdmin(ImportExportActionModelAdmin):
    list_display = ("id", "name", "status", "user", "profession", "money", "public_date")
    list_select_related = ("user", "profession")

    search_fields = (
        "id",
        "requirements",
        "name",
        "conditions"
    )
    list_filter = ("status", "accommodation", "food", "drive", )
    date_hierarchy = "public_date"

    exclude = ("slug", "count_see", "count_sentence", )
    resource_class = VacancyResource


@admin.register(Questionnaire)
class QuestionnaireAdmin(ImportExportActionModelAdmin):
    search_fields = (
        "id",
        "description"
    )
    list_display = ("id", "status", "user", "profession", "public_date")
    list_select_related = ("user", "profession")

    list_filter = ("health_book", "vaccinated", "no_profession", "not_citizen", "self_propelled")
    date_hierarchy = "public_date"

    exclude = ("slug", "count_see", "count_sentence",)
    resource_class = QuestionnaireResource

