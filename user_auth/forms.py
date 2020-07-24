from allauth.account.forms import SignupForm, LoginForm, ResetPasswordForm, ChangePasswordForm, ResetPasswordKeyForm
from django import forms
from phonenumber_field.formfields import PhoneNumberField
import phonenumbers
from django.forms import ValidationError
my_default_errors = {
    'required': 'Это поле обязательно к заполнению',
    'invalid': 'Номер телефона должен быть введен в формате: +77777777777'
}
class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    first_name = forms.CharField(label='Имя', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Имя'}), required=True)
    last_name = forms.CharField(label='Фамилия', max_length=50,
                                widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}), required=True)

    phone = PhoneNumberField(label='Телефон', widget=forms.TextInput(attrs={'placeholder': 'Пример: +77777777777'}), error_messages=my_default_errors, required=True)




class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            if visible.name == 'remember':
                visible.field.widget.attrs['class'] = 'custom-control-input'
            # visible.label = None


class CustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.label = None


class CustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.label = None


class CustomResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordKeyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.label = None
