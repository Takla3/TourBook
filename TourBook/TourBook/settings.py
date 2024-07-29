"""
Django settings for TourBook project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import cloudinary
from datetime import timedelta
from pathlib import Path
import os
import dj_database_url
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-d4v#k_pwdnqp3-0wu-3cfbaz+a$k$98-x0@wmn4p8ukw_ybj@0'

# SECURITY WARNING: don't run with debug turned on in production!


DEBUG = True

if DEBUG:

    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'djoser',
    'accounts',
    'Advertiser',
    'Tour_Organizer',
    'Client',
    'Core',
    'django_cleanup.apps.CleanupConfig',
    'cloudinary_storage',
    'cloudinary',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'TourBook.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'TourBook.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'TourBook'.lower(),
#         'USER': 'postgres',
#         'PASSWORD': '1234',
#         'HOST': 'localhost',
#         'PORT': 5432,
#     }
# }
DATABASES = {
    'default': dj_database_url.config(
        # Replace this value with your local database's connection string.
        default='postgresql://tourbook_ffi9_user:FEidGVybo60YCqDHN66K3pPqrU2Taxja@dpg-cqfutdpu0jms7388ker0-a/tourbook_ffi9',
        conn_max_age=600
    )
}
# DATABASES = {
#     "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
# }
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "koykhaled@gmail.com"
EMAIL_HOST_PASSWORD = "oepx iomz rzzu ehym"
EMAIL_USE_TLS = True


DJOSER = {
    # login should be with email field
    'LOGIN_FIELD': 'username',

    # make user confirm his password
    'USER_CREATE_PASSWORD_RETYPE': True,

    # you need to pass re_new_username to /users/set_username/ endpoint, to validate username equality.
    'SET_USERNAME_RETYPE': True,

    # you need to pass re_new_password to /users/set_password/ endpoint, to validate password equality.
    'SET_PASSWORD_RETYPE': True,

    'PASSWORD_RESET_CONFIRM_RETYPE': True,

    # to send email confirmation for users when he want to change his password
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,

    # route to send email message when user need to change his password
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',

    # to send email confirmation for users when he want to change his email
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,

    # to send confirmation email when user register
    'SEND_CONFIRMATION_EMAIL': True,

    # route to change username
    'USERNAME_RESET_CONFIRM_URL': 'username/reset/confirm/{uid}/{token}',

    # to activate user after registeration
    'ACTIVATION_URL': 'activate/{uid}/{token}',

    # to recive activation email
    'SEND_ACTIVATION_EMAIL': True,
    'SERIALIZERS': {
        'user_create': 'accounts.serializers.UserRegisterSerializer',
        'user': 'accounts.serializers.UserSerializer',
        'current_user': 'accounts.serializers.UserSerializer',
        'user_delete': 'djoser.serializers.UserDeleteSerializer',
    },
}

REST_FRAMEWORK = {
    # user should be authenticated before getting access to any route
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


# Media File Directory for store files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'Core.UserAccount'


SPECTACULAR_SETTINGS = {
    'TITLE': "TourBook API's",
}


CLOUDINARY_STORAGE = {
    'CLOUD_NAME': "dntpfwkri",
    'API_KEY': "345918894245781",
    'API_SECRET': "DO-7twxcq8ncg1FLMwxVlHpO9E4"
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

STATIC_URL = '/static/'

# This production code might break development mode, so we check whether we're in DEBUG mode
if not DEBUG:
    # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
    # and renames the files with unique names for each version to support long-term caching
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# CORS_ORIGIN_WHITELIST = [
#     'http://localhost:5173',  # Replace with your frontend host
# ]

CORS_ALLOW_ALL_ORIGINS = True
