from allauth.account.forms import SignupForm, LoginForm, ResetPasswordForm, ChangePasswordForm, ResetPasswordKeyForm
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import User
import phonenumbers
from django.forms import ValidationError

my_default_errors = {
    'required': 'Это поле обязательно к заполнению',
    'invalid': 'Номер телефона должен быть введен в формате: +77777777777'
}


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    first_name = forms.CharField(label='Имя', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Имя'}),
                                 required=True)
    last_name = forms.CharField(label='Фамилия', max_length=50,
                                widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}), required=True)
    phone = PhoneNumberField(label='Телефон', widget=forms.TextInput(attrs={'placeholder': 'Пример: +77777777777'}),error_messages=my_default_errors, required=True)
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'placeholder': 'E-mail'}), required=True)


class UserResetPasswordForm(forms.Form):
    # class Meta:
    #     model = User
    #     fields = ['phone']
    def __init__(self, *args, **kwargs):
        super(UserResetPasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    phone = PhoneNumberField(label='Телефон', widget=forms.TextInput(attrs={'placeholder': 'Пример: +77777777777'}),error_messages=my_default_errors, required=True)


class CustomLoginForm(LoginForm):
    error_messages = {
        'username_password_mismatch': ("Телефон номер пользователя и/или пароль не верны."),
        'required': 'Это поле обязательно к заполнению',
        'invalid': 'Номер телефона должен быть введен в формате: +77777777777'
    }

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

            if visible.name == 'login':
                print(visible.subwidgets)
                visible.label = 'Телефон номер'
                visible.field.widget.attrs['placeholder'] = 'Пример: +77777777777'
                visible.field.error_message = my_default_errors
            if visible.name == 'remember':
                visible.field.widget.attrs['class'] = 'custom-control-input'

            # visible.label = None


class CustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():

            visible.field.widget.attrs['class'] = 'form-control'
            # visible.label = None


class CustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



class CustomResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordKeyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.label = None
