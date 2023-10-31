from django.core.management.utils import get_random_secret_key
from .base import *  # noqa # pylint: disable=unused-wildcard-import
from app.settings.local import DATABASES
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ["*"]
# os.environ['GDAL_LIBRARY_PATH'] = '/usr/lib/libgdal.so'  # Replace this path with the actual path to libgdal.so on your system

# Generate a new SECRET_KEY if it's not already set
# SECRET_KEY = get_random_secret_key()
# DATABASES = DATABASES
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(weeks=521),  # 10 years
#     "REFRESH_TOKEN_LIFETIME": timedelta(weeks=521),
# }