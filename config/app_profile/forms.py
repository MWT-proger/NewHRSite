from django import forms
from .models import ProjectStartUp, Country
from app_account.models import User


class ProjectStartUpForm(forms.ModelForm):
    logo = forms.ImageField(error_messages={'required': 'Необходимо выбрать лого для проекта!'})
    # youtube = forms.CharField(error_messages={'required': 'Вставте ссылку на youtube!'})
    user_2 = forms.ModelChoiceField(required=False, queryset=None, label="Фаундер №2")
    user_3 = forms.ModelChoiceField(required=False, queryset=None, label="Фаундер №3")

    def __init__(self, *args, **kwargs):
        super(ProjectStartUpForm, self).__init__(*args, **kwargs)
        self.fields['user_2'].queryset = User.objects.filter(is_superuser=False, is_active=True)
        self.fields['user_3'].queryset = User.objects.filter(is_superuser=False, is_active=True)
        self.fields['user_2'].widget.attrs.update({'class': 'js-example-basic-single w-100'})
        self.fields['user_2'].widget.attrs.update({'data-width': '100%'})
        self.fields['user_3'].widget.attrs['class'] = 'js-example-basic-single w-100'
        self.fields['user_3'].widget.attrs.update({'data-width': '100%'})
        self.fields['technology'].widget.attrs['class'] = 'js-example-basic-multiple w-100'
        self.fields['technology'].widget.attrs.update({'data-width': '100%'})
        self.fields['technology'].widget.attrs.update({'multiple': 'multiple'})
        self.fields['views_sport'].widget.attrs['class'] = 'js-example-basic-multiple w-100'
        self.fields['views_sport'].widget.attrs.update({'data-width': '100%'})
        self.fields['views_sport'].widget.attrs.update({'multiple': 'multiple'})


    class Meta:
        model = ProjectStartUp
        exclude = ('user_1', 'public_date',)


class ProjectStartUpUpdateForm(forms.ModelForm):
    logo = forms.ImageField(error_messages={'required': 'Необходимо выбрать лого для проекта!'})
    # youtube = forms.CharField(error_messages={'required': 'Вставте ссылку на youtube!'})
    user_2 = forms.ModelChoiceField(required=False, queryset=None, label="Фаундер №2")
    user_3 = forms.ModelChoiceField(required=False, queryset=None, label="Фаундер №3")

    def __init__(self, *args, **kwargs):
        super(ProjectStartUpUpdateForm, self).__init__(*args, **kwargs)

        self.fields['user_2'].queryset = User.objects.filter(is_superuser=False, is_active=True)
        self.fields['user_3'].queryset = User.objects.filter(is_superuser=False, is_active=True)
        self.fields['user_2'].widget.attrs.update({'class': 'js-example-basic-single w-100'})
        self.fields['user_2'].widget.attrs.update({'data-width': '100%'})
        self.fields['user_3'].widget.attrs['class'] = 'js-example-basic-single w-100'
        self.fields['user_3'].widget.attrs.update({'data-width': '100%'})
        self.fields['technology'].widget.attrs['class'] = 'js-example-basic-multiple w-100'
        self.fields['technology'].widget.attrs.update({'data-width': '100%'})
        self.fields['technology'].widget.attrs.update({'multiple': 'multiple'})
        self.fields['views_sport'].widget.attrs['class'] = 'js-example-basic-multiple w-100'
        self.fields['views_sport'].widget.attrs.update({'data-width': '100%'})
        self.fields['views_sport'].widget.attrs.update({'multiple': 'multiple'})


    class Meta:
        model = ProjectStartUp
        exclude = ('user_1', 'public_date', 'tracks', 'works', 'likes',)
