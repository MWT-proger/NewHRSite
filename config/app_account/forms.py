from crispy_forms.helper import FormHelper
from django.contrib.auth import get_user_model
from django import forms
from crispy_forms.layout import Layout, Submit, Row, Column, Button

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


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(label='Номер телефона' )

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('third_name', css_class='form-group col-md-6 mb-0'),
                Column('age', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Сохранить', css_class='btn btn-primary m-1 col-12 col-md-auto'),
            Button('cancel', 'Сменить номер телефона', css_class='btn btn-outline-danger m-1 col-12 col-md-auto')
        )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'third_name', 'age', 'username', 'email']


class UserEmployerUpdateForm(forms.ModelForm):
    username = forms.CharField(label='Номер телефона')

    def __init__(self, *args, **kwargs):
        super(UserEmployerUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('third_name', css_class='form-group col-md-6 mb-0'),
                Column('username', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('name_company', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Сохранить')
        )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'third_name', 'username', 'email', 'name_company']
