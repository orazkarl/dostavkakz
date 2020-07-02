from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class User(AbstractUser):
    email = models.EmailField('E-mail', max_length=100, unique=True)
    phone = PhoneNumberField('Телефон', unique=True, help_text='Номер телефона должен быть введен в формате: +77777777777')




