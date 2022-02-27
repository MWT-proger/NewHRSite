import re

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from django.core.exceptions import ValidationError

from .models import Questionnaire, Vacancy, WorkMode, City, Region, Profession


class RangeField(Field):
    template = "app_profile/include/field_range_driver.html"


class RangeFieldTotalService(Field):
    template = "app_profile/include/field_range_total_service.html"


class RangeFieldMoneyFrom(Field):
    template = "app_profile/include/field_range_money_from.html"


class RangeFieldMoneyTo(Field):
    template = "app_profile/include/field_range_money_to.html"


class QuestionnaireBaseForm(forms.ModelForm):
    driving_experience = forms.IntegerField(label='Водительский стаж',
                                            widget=forms.NumberInput(attrs={'type': 'range',
                                                                            'step': '1',
                                                                            'value': '0',
                                                                            'class': 'range-slider__range',
                                                                            'min': '0',
                                                                            'max': '50'}),
                                            required=False)
    total_service = forms.IntegerField(label='Общий стаж',
                                       widget=forms.NumberInput(attrs={'type': 'range',
                                                                       'step': '1',
                                                                       'value': '0',
                                                                       'class': 'range-slider__range',
                                                                       'min': '0',
                                                                       'max': '50'}),
                                       required=False)

    def __init__(self, *args, **kwargs):
        super(QuestionnaireBaseForm, self).__init__(*args, **kwargs)
        self.fields['driver_license'].widget.attrs.update({'class': 'js-example-basic-single w-100'})
        self.fields['driver_license'].widget.attrs.update({'data-width': '100%'})
        self.fields['driver_license'].widget.attrs.update({'multiple': 'multiple'})

        self.fields['region'].widget.attrs.update({'class': 'js-example-basic-single w-100 select form-control'})
        self.fields['region'].widget.attrs.update({'data-width': '100%'})

        self.fields['city'].widget.attrs.update({'class': 'js-example-basic-single w-100 select form-control'})
        self.fields['city'].widget.attrs.update({'data-width': '100%'})

        self.fields['profession'].widget.attrs.update({'class': 'js-example-basic-single w-100 select form-control'})
        self.fields['profession'].widget.attrs.update({'data-width': '100%'})

        self.fields['phone'].widget.attrs.update({'data-rule-required': 'true'})
        self.fields['phone'].widget.attrs.update({'data-inputmask-alias': '+7(999)999-9999'})

        self.helper = FormHelper()
        self.helper.layout = Layout(

            Row(
                Column('region', css_class='form-group col-md-6 mb-0'),
                Column('city', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('driver_license', css_class='form-group col-md-6 mb-0'),
                Column(RangeField("driving_experience"), css_class='form-group col-md-6 mb-0 '),
                css_class='form-row'
            ),
            Row(
                Column('phone', css_class='form-group col-md-6 mb-0'),
                Column(RangeFieldTotalService("total_service"), css_class='form-group col-md-6 mb-0 '),
                css_class='form-row'
            ),

            Row(
                Column('profession', css_class='form-group col-md-6 mb-0'),
                Column('', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('health_book', css_class='form-group col-md-6 mb-0'),
                Column('vaccinated', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('not_citizen', css_class='form-group col-md-6 mb-0'),
                Column('no_profession', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('self_propelled', css_class='form-group col-md-6 mb-0'),
                Column('', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Сохранить')
        )

    def clean_phone(self):
        data = self.cleaned_data['phone']
        if not re.match(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$', data):
            raise ValidationError("Введите правильный номер телефона")
        return data

    class Meta:
        model = Questionnaire
        exclude = ('user', 'public_date', 'status', 'count_see',)


class QuestionnaireCreateForm(QuestionnaireBaseForm):
    pass


class QuestionnaireUpdateForm(QuestionnaireBaseForm):
    status = forms.CharField(required=False)

    class Meta:
        model = Questionnaire
        exclude = ('user', 'public_date', 'count_see',)


class QuestionnaireDeleteForm(forms.ModelForm):

    class Meta:
        model = Questionnaire
        fields = ('profession',)


# Раздел для Работодателя


class VacancyBaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(VacancyBaseForm, self).__init__(*args, **kwargs)
        self.fields['region'].widget.attrs.update({'class': 'js-example-basic-single w-100 select form-control'})
        self.fields['region'].widget.attrs.update({'data-width': '100%'})

        self.fields['city'].widget.attrs.update({'class': 'js-example-basic-single w-100 select form-control'})
        self.fields['city'].widget.attrs.update({'data-width': '100%'})

        self.fields['profession'].widget.attrs.update({'class': 'js-example-basic-single w-100 select form-control'})
        self.fields['profession'].widget.attrs.update({'data-width': '100%'})

        self.fields['work_mode'].widget.attrs.update({'class': 'js-example-basic-single w-100 select form-control'})
        self.fields['work_mode'].widget.attrs.update({'data-width': '100%'})

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('profession', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('region', css_class='form-group col-md-6 mb-0'),
                Column('city', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('work_mode', css_class='form-group col-md-6 mb-0'),
                Column('money', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),


            Row(
                Column('accommodation', css_class='form-group col-md-6 mb-0'),
                Column('food', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('drive', css_class='form-group col-md-6 mb-0'),
                Column('', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('requirements', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('conditions', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Сохранить')
        )

    class Meta:
        model = Vacancy
        exclude = ('user', 'public_date', 'status', 'count_see',)


class VacancyCreateForm(VacancyBaseForm):
    pass


class VacancyUpdateForm(VacancyBaseForm):
    status = forms.CharField(required=False)

    class Meta:
        model = Vacancy
        exclude = ('user', 'public_date', 'count_see',)


class VacancyDeleteForm(forms.ModelForm):

    class Meta:
        model = Vacancy
        fields = ('profession',)


class FilterVacancyForm(forms.ModelForm):
    regions = forms.ModelMultipleChoiceField(label='Регион',
                                             required=False,
                                             queryset=Region.objects.all(),
                                             )
    citys = forms.ModelMultipleChoiceField(label='Город',
                                           required=False,
                                           queryset=City.objects.all(),
                                           )
    work_modes = forms.ModelMultipleChoiceField(label='Режим работы',
                                                required=False,
                                                queryset=WorkMode.objects.all(),
                                                )
    professions = forms.ModelMultipleChoiceField(label='Профессия',
                                                 required=False,
                                                 queryset=Profession.objects.all(),
                                                 )
    # city = forms.ModelChoiceField(label='Город', required=False, queryset=City.objects.all())
    # work_mode = forms.ModelChoiceField(label='Режим работы', required=False, queryset=WorkMode.objects.all())
    money_from = forms.CharField(label='ЗП от', required=False, help_text='В рублях')
    money_to = forms.IntegerField(label='ЗП до', required=False, initial=999999)

    def __init__(self, *args, **kwargs):
        super(FilterVacancyForm, self).__init__(*args, **kwargs)

        self.fields['regions'].widget.attrs.update({'class': 'js-example-basic-single w-100'})
        self.fields['regions'].widget.attrs.update({'data-width': '100%'})
        self.fields['regions'].widget.attrs.update({'multiple': 'multiple'})

        self.fields['citys'].widget.attrs.update({'class': 'js-example-basic-single w-100'})
        self.fields['citys'].widget.attrs.update({'data-width': '100%'})
        self.fields['citys'].widget.attrs.update({'multiple': 'multiple'})

        self.fields['professions'].widget.attrs.update({'class': 'js-example-basic-single w-100'})
        self.fields['professions'].widget.attrs.update({'data-width': '100%'})
        self.fields['professions'].widget.attrs.update({'multiple': 'multiple'})

        self.fields['work_modes'].widget.attrs.update({'class': 'js-example-basic-single w-100'})
        self.fields['work_modes'].widget.attrs.update({'data-width': '100%'})
        self.fields['work_modes'].widget.attrs.update({'multiple': 'multiple'})

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('regions', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('citys', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('professions', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('work_modes', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(RangeFieldMoneyFrom('money_from'), css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(RangeFieldMoneyTo('money_to'), css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('accommodation', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('food', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('drive', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Показать')
        )

    class Meta:
        model = Vacancy
        exclude = ('user', 'status', 'count_see', 'region', 'city', 'profession', 'work_mode',)
