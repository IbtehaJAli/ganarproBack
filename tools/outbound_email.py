import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import django
from salesforce_functions import expose_django_settings
from decouple import config
expose_django_settings()
from app.api.authentication.models import User
from salesforce_functions import expose_django_settings
from datetime import datetime

from django.utils.text import slugify
from sentry_sdk import capture_exception

from app.api.projects.models import ContactRole, Opportunity
from salesforce_functions import expose_django_settings


users = User.objects.all().prefetch_related("profile")
try:
    for user in users:
        print(f"user {user.email}")
        user.profile.outbound_email = user.email
        user.profile.save()
except Exception as e:
    print(e)

