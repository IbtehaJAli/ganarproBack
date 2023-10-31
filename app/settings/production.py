import os

from .base import *
import django_heroku
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = os.getenv("DEBUG")
ALLOWED_HOSTS = ['https://app.ganarpro.com', 'https://api.ganarpro.com']

# Application definition


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
    }
}

## ------------------- HEROKU----------------------
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT')
django_heroku.settings(locals())

# ## --------------------------SENDGRID-----------------------
# EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
# SENDGRID_API_KEY = os.getenv('SENDGRID_KEY', '')
# SENDGRID_SANDBOX_MODE_IN_DEBUG = False
# SENDGRID_TRACK_CLICKS_HTML = False
# SENDGRID_TRACK_CLICKS_PLAIN = False
# DEFAULT_FROM_EMAIL = 'Support Team <support@ganarpro.com>'
if os.getenv('ENV') == "STAGING":
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # ---------------------MAILGUN--------------------- #
    ANYMAIL = {
        # (exact settings here depend on your ESP...)
        "MAILGUN_API_KEY": os.getenv('MAIL_GUN'),
    }
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
    # DEFAULT_FROM_EMAIL = "support@ganarpro.com"
    # SERVER_EMAIL = "support@ganarpro.com"

DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STRIPE_LIVE_MODE = True
STRIPE_LIVE_SECRET_KEY = os.getenv("STRIPE_LIVE_SECRET_KEY")
STRIPE_LIVE_PUBLIC_KEY = os.environ.get("STRIPE_LIVE_PUBLIC_KEY")

sentry_sdk.init(
    dsn="https://33bbe4759ad4415784682f5d9de477bb@o395280.ingest.sentry.io/6702765",
    integrations=[
        DjangoIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
