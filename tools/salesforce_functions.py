import sys
import os

import django
from decouple import config

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# print(sys.path)
from datetime import datetime

from django.conf import settings
from phonenumbers import geocoder
import phonenumbers

from app.api.projects.states import us, uk, ca
from itertools import chain

state_list = list(chain(us, ca, uk))


def fixDate(datestr):
    dateobj = datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%S.000+0000')
    formatedDate = dateobj.strftime('%B %d %Y')
    return formatedDate


def fixStatusUpdateDate(datestr):
    if datestr == None:
        return datestr
    dateobj = datetime.strptime(datestr, '%Y-%m-%d')
    formatedDate = dateobj.strftime('%B %d %Y')
    return formatedDate


def get_region_name(state):
    if state:
        state_value = state.split(', ')[1]
        for x in state_list:
            if x['abbreviation'] == state_value:
                return x['name']
    return state


def phone_clean_up(phone):
    if phone:
        return phone.replace('Phone:', '').replace('.', '').replace('(', '').replace(')', '').replace(' ', '').replace(
            '-', '')
    return None


def single_contact(contact):
    contact_phone = phone_clean_up(contact)
    format_text_country = 'US'
    # if contact.country and (contact.country.lower() == str('United Kingdom').lower() or contact.country.lower() == str('UK').lower()):
    #     format_text_country = 'UK'
    # elif contact.country and (contact.country.lower() == str('Canada').lower() or contact.country.lower() == str('CA').lower()):
    #     format_text_country = 'CA'

    region = None
    try:
        phone_number = phonenumbers.parse(contact_phone, format_text_country) if contact_phone else None
        region = geocoder.description_for_number(phone_number,
                                                 "en") if phone_number and phonenumbers.is_possible_number(
            phone_number) and phonenumbers.is_valid_number(phone_number) else None
    except:
        pass
    # update region
    return get_region_name(region) if region and ',' in region else region


def single_opportunity(state_short):
    country_short = [x['country_short'] for x in state_list if x['abbreviation'] == state_short]
    return country_short[0] if len(country_short) > 0 else None


def expose_django_settings():

    DEBUG = config('DEBUG', '', cast=bool)
    print(DEBUG)
    if DEBUG:
        print('HERE')
        from app.settings.local import DATABASES, INSTALLED_APPS
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings.local'
        # settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
    else:
        from app.settings.production import DATABASES, INSTALLED_APPS
    django.setup()




