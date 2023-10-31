"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
import cloudinary
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_NAME', default='drtsq1r46'),
    api_key=os.getenv('CLOUDINARY_API_KEY', default='775748257968187'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET', default='986Lml_WKTW7ZEZy-1BkHkA_8tg'),
    secure=True,
)
# Application definition

DJANGO_APPS = [

    "django.contrib.contenttypes",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.gis',
    'django.contrib.postgres'
]
LOCAL_APPS = [
    "app.api.authentication",
    "app.api.users",
    "app.api.proposal",
    "app.api.project_type",
    "app.api.mortgage_calculator",
    "app.api.gcqualify",
    "app.api.projects",
    "app.api.contact_roles",
    "app.api.company_details",
    "app.api.email_templates",
    "app.api.emails",
    "app.api.capabilities_statement",
    "app.api.gc_planify",
]
THIRD_PARTY_APPS = [
    'ckeditor',
    "rest_framework",
    "drf_yasg",
    "rest_framework_swagger",
    "import_export",
    "djstripe",
    "django_rest_passwordreset",
    "storages",
    'cloudinary_storage',
    'cloudinary',
    "anymail",
    'django_celery_results',
    'django_celery_beat',


]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "authentication.User"
STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles/")
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(weeks=521),  # 10 years
    "REFRESH_TOKEN_LIFETIME": timedelta(weeks=521),
}

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
}

CORS_ORIGIN_ALLOW_ALL = True
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
APPEND_SLASH = False

DJSTRIPE_WEBHOOK_SECRET = "whsec_xxx"  # We don't use this, but it must be set
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"

STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')

SENDGRID_TRACK_CLICKS_HTML = True
SENDGRID_TRACK_CLICKS_PLAIN = True
HASHID_FIELD_SALT = '4)@+y0^v&&xnl(*hqb&uz-n!=w^=xh32_%#ynu866znva1hn3g'
BASE_URL = os.getenv('BASE_URL')
STRIPE_CUS_ID = os.getenv('STRIPE_CUS_ID')
TIME_ZONE = 'America/New_York'
MEDIA_URL = '/media/'  # or any prefix you choose
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.RawMediaCloudinaryStorage'
REDIS_URL = os.getenv('REDIS_URL', default='')
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
# CELERY_RESULT_BACKEND = 'django-db'
# CELERY_CACHE_BACKEND = 'django-cache'
# CELERY_BROKER_URL = "redis://localhost:6379"
# CELERY_RESULT_BACKEND = "redis://localhost:6379"
