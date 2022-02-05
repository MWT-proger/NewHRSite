from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Номер телефона')
    name_company = forms.CharField(label='Наименование компании', required=False)
    email = forms.EmailField(label='Адрес Электронной почты')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Пароль ещё раз', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'name_company', 'email', 'password', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароль не совпадает')
        return cd['password2']


class UserResetPasswordForm(forms.Form):
    username = forms.CharField(label='Номер телефона')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Пароль ещё раз', widget=forms.PasswordInput)

    class Meta:
        fields = ('username', 'password', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароль не совпадает')
        return cd['password2']
