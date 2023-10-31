
import os
from .base import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = os.getenv("DEBUG")

ALLOWED_HOSTS = ['*']

# Application definition
# dev.py; add these lines
INSTALLED_APPS = INSTALLED_APPS + [
    # 'debug_toolbar',
    'silk',
]
MIDDLEWARE = MIDDLEWARE + [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'silk.middleware.SilkyMiddleware',
]

INTERNAL_IPS = "127.0.0.1:8001"
DEBUG_TOOLBAR_CONFIG = {'INSERT_BEFORE':'</head>'}

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.getenv("DB_NAME"),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST"),
        "USER": os.getenv("DB_USER"),
        "PORT": os.getenv("DB_PORT"),
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATIC_URL = '/static/'
#
# # Extra places for collectstatic to find static files.
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )
# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
# ########        stripe #########


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
# MAILGUN_ACCESS_KEY = '6d8d428c-7027d979'
# MAILGUN_SERVER_NAME = 'mail.ganarpro.com'

# EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"

# # ---------------------MAILGUN--------------------- #
# ANYMAIL = {
#     # (exact settings here depend on your ESP...)
#     "MAILGUN_API_KEY": os.getenv('MAIL_GUN'),
#     # "MAILGUN_SENDER_DOMAIN": 'mail.ganarpro.com',
# }
# # EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
# DEFAULT_FROM_EMAIL = "support@ganarpro.com"
# SERVER_EMAIL = "support@ganarpro.com"

# --------------------------SENDGRID-----------------------
# EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
# SENDGRID_API_KEY = os.getenv('SENDGRID_KEY')
# SENDGRID_SANDBOX_MODE_IN_DEBUG = False
# SENDGRID_TRACK_CLICKS_HTML = False
# SENDGRID_TRACK_CLICKS_PLAIN = False
# DEFAULT_FROM_EMAIL = 'Support Team <support@ganarpro.com>'


###-------------------SENTRY---------------###
# sentry_sdk.init(
#     dsn="",
#     integrations=[],
#
#     # If you wish to associate users to errors (assuming you are using
#     # django.contrib.auth) you may enable sending PII data.
#     send_default_pii=False
# )
# sentry_sdk.init(
#     dsn="https://11add338ccc345c6a402cd8cb20d2bc1@o395280.ingest.sentry.io/5246837",
#     integrations=[DjangoIntegration()],
#
#     # If you wish to associate users to errors (assuming you are using
#     # django.contrib.auth) you may enable sending PII data.
#     send_default_pii=True
# )
STRIPE_LIVE_MODE = False
STRIPE_TEST_SECRET_KEY = os.getenv("STRIPE_TEST_SECRET_KEY", "")
STRIPE_TEST_PUBLIC_KEY = os.environ.get("STRIPE_TEST_PUBLIC_KEY", "")