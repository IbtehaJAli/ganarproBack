import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.local")

django.setup()