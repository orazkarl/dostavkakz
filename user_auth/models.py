from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from dostavkakz.settings import AUTH_USER_MODEL


# Create your models here.


class User(AbstractUser):
    email = models.EmailField('E-mail', max_length=100, unique=True)
    phone = PhoneNumberField('Телефон', unique=True,
                             help_text='Номер телефона должен быть введен в формате: +77777777777')
    # address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    address_name = models.CharField('Адрес', max_length=250, null=True, blank=True)
    number_house = models.CharField('Номер дома', max_length=10, null=True, blank=True)
    number_apartment = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField('Статус', max_length=100, null=True, blank=True)

    def __str__(self):
        return self.address_name