"""
Django settings for PathFinder project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get('SECRET_KEY', 'shawarma')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = bool(int(os.environ.get('DEBUG', 1)))

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Security measure to prevent HTTP Host header attacks (see https://docs.djangoproject.com/en/4.1/ref/settings/#allowed-hosts)
# Only when DEBUG is False, the ALLOWED_HOSTS list is used
ALLOWED_HOSTS = ['143.198.222.14', 'localhost',
                 'www.pathfinder.ink', 'pathfinder.ink', '127.0.0.1']
ALLOWED_HOSTS.extend(
    filter(None, os.environ.get('ALLOWED_HOSTS', '').split(',')))

PYTHONUNBUFFERED = 0
# Application definition

#for google sign in
SITE_ID = 2

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # below entry added so django knows about the app and its config
    'PathFinder.PathFinderApp.apps.PathfinderappConfig',
    #This is for the google sign up
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    
]

#google sign up pt2
SOCIALACCOUNT_PROVIDERS = {
    "google":{
    "SCOPE": [
    "profile",
    "email"
    ],
    "AUTH_PARAMS": {"access_type": "online"}
    }
}

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'PathFinder.PathFinderBase.wsgi.application'
ASGI_APPLICATION = 'PathFinder.PathFinderBase.asgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
# These are the credentials for the local psql database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # pathfinderdb on remote server, only diff
        # 'NAME': os.environ.get('DB_NAME', 'pathfinderdb'),
        'NAME': os.environ.get('DB_NAME', 'AppDBdjango'),
        'USER': os.environ.get('DB_USER', 'pathfinderdbsu'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'pa$$wordFinder'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('SQL_PORT', 5432),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, '/static/')
STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

ROOT_URLCONF = 'PathFinder.PathFinderBase.urls'


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    # os.path.join(BASE_DIR, 'static/pathfinderapp'),
    # os.path.join(BASE_DIR, 'static/admin')
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#google sign up pt3

SOCIALACCOUNT_LOGIN_ON_GET=True

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend"
)

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

GOOGLE_CLIENT_ID = '320096241471-1o3b72no3kk8raqqg204qj9k07q3ss8c.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_TOKEN_URI = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URI = 'https://www.googleapis.com/oauth2/v1/userinfo'
GOOGLE_REDIRECT_URI = 'http://localhost:8000/google-auth-callback'