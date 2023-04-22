import re
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django import forms

from sitestorage.models import PaymentOrder


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='', widget=forms.EmailInput(
        attrs={'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
               'placeholder': 'E-mail'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
               'placeholder': "Пароль"}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
               'placeholder': "Подтверждение пароля"}))
    type = forms.CharField(widget=forms.TextInput(attrs={'type': "hidden", 'value': 'registration'}))

    class Meta:
        model = get_user_model()
        fields = ('email',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserAuthorizationForm(forms.ModelForm):
    email = forms.EmailField(label='', widget=forms.EmailInput(
        attrs={'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
               'placeholder': 'E-mail'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control  border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
               'placeholder': "Пароль"}))
    type = forms.CharField(widget=forms.TextInput(attrs={'type': "hidden", 'value': 'login'}))

    class Meta:
        model = get_user_model()
        fields = ('email',)


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'phone', 'password')


def validate_card_number(value):
    if not re.match(r'^[0-9]{12,19}$', value):
        raise ValidationError('Не верный номер карты')


def validate_card_month(value):
    if not re.match(r'^\d\d$', value) or not 0 < int(value) <= 12:
        raise ValidationError('Не верный месяц')


def validate_card_year(value):
    if not re.match(r'^\d\d$', value) or not 23 <= int(value) < 99:
        raise ValidationError('Не верный год')


def validate_card_holder(value):
    if not re.match(r'^[a-zA-Z\s]{1,26}$', value):
        raise ValidationError('Не верное имя держателя карты')


def validate_card_cvc(value):
    if not re.match(r'^\d{3,4}$', value):
        raise ValidationError('Не верный код CVC')


class PaymentForm(forms.ModelForm):
    card_number = forms.CharField(
        validators=[validate_card_number],
        widget=forms.TextInput(attrs={'placeholder': 'Введите номер'})
    )
    card_month = forms.CharField(
        validators=[validate_card_month],
        widget=forms.TextInput(attrs={'placeholder': 'ММ'})
    )
    card_year = forms.CharField(
        validators=[validate_card_year],
        widget=forms.TextInput(attrs={'placeholder': 'ГГ'})
    )
    card_holder = forms.CharField(
        validators=[validate_card_holder],
        widget=forms.TextInput(attrs={'placeholder': 'Имя владельца'})
    )
    card_cvc = forms.CharField(
        validators=[validate_card_cvc],
        widget=forms.TextInput(attrs={'placeholder': 'CVC'})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'pochta@mail.ru'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'order__form_input orderStep_form_input'

    class Meta:
        model = PaymentOrder
        fields = ['card_number', 'card_month', 'card_year', 'card_holder', 'card_cvc', 'email']
