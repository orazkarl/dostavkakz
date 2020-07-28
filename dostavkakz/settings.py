"""
Django settings for dostavkakz project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p-fn#zm9!h2dhljbc!6*n)s3qahxg+ls)&oa00ev(zs0n77j71'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'landing',
    # 'landing.apps.LandingConfig',
    'user_auth.apps.UserAuthConfig',
    'api1c.apps.Api1CConfig',
    'order.apps.OrderConfig',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'phonenumber_field',

    'cart',
    'django_2gis_maps',

    'rest_framework',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'geoip2_extras.middleware.GeoIP2Middleware',

]

ROOT_URLCONF = 'dostavkakz.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],

        },
    },
]

WSGI_APPLICATION = 'dostavkakz.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'jetkizudb',
        'USER': 'admin',
        'PASSWORD': '123admin',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Almaty'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Sendgrid
# SENDGRID_API_KEY = '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'
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_HOST_USER = 'apikey'
# EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
# EMAIL_PORT = 2525
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = 'noreply@getall.kz'

ACCOUNT_EMAIL_VERIFICATION = 'none'
SITE_ID = 1
AUTH_USER_MODEL = 'user_auth.User'
# ACCOUNT_AUTHENTICATION_METHOD = 'phone'
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username'
# ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
# ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400  # 1 day in seconds
# ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/'
# ACCOUNT_ADAPTER = 'user_auth.adapter.AccountAdapter'

ACCOUNT_FORMS = {
    'login': 'user_auth.forms.CustomLoginForm',
    'signup': 'user_auth.forms.CustomSignupForm',
    # 'add_email': 'allauth.account.forms.AddEmailForm',
    'change_password': 'user_auth.forms.CustomChangePasswordForm',
    # 'set_password': 'allauth.account.forms.SetPasswordForm',
    'reset_password': 'user_auth.forms.CustomResetPasswordForm',
    # 'reset_password_from_key': 'user_auth.forms.CustomResetPasswordKeyForm',
    # 'disconnect': 'allauth.socialaccount.forms.DisconnectForm',
}

CART_SESSION_ID = 'cart'

# mobizon
# MOBIZON_DOMEN = 'api.mobizon.kz'
# MOBIZON_KEY = 'kz985662942c6d4ac5f9e63cb39d2f57f7a21ed8c69ae360fd93d01205cec0935057a5'


COURIER_TELEGRAM_BOT_TOKEN = '1307138365:AAGtwTSrMWlXIGtrEqbzRnIelXHA1IE0EWY'
