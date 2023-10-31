import os
import re
import sys
import time
import urllib3
import argparse
import requests
import pprint
import threading


from django.conf import settings



from database_connections import dbinit, init
from decouple import config
from salesforce_opportunity import opportunity_migrate

from salesforce_account import account_migrate
from salesforce_contact import contact_migrate
from salesforce_contact_roles import contactrole_migrate


if __name__ == '__main__':
    import sentry_sdk


    sentry_sdk.init(dsn="https://33bbe4759ad4415784682f5d9de477bb@o395280.ingest.sentry.io/6702765")
    env = ''
    # parser = argparse.ArgumentParser("sf_import_data.py")
    # parser.add_argument("--env", help="The environemnt to run this script for dev, stage, prod", type=str)
    # args = parser.parse_args()
    # if args.env:
    #     env = args.env

    database = config('DB_NAME')
    debug = config('DEBUG')
    con = dbinit()
    sf = init()
    cur = con.cursor()
    from sentry_sdk import capture_exception

    try:
        opportunity_migrate(con, cur, sf)
        # # # migrate contact records to django
        # contact_migrate(con, cur, sf)
        # # migrate account records to django
        # account_migrate(con, cur, sf)
        # # #
        # # # # # migrate contact role records to django
        # contactrole_migrate(con, cur, sf)
    except (Exception, KeyboardInterrupt) as e:
        # Alternatively the argument can be omitted
        if not debug:
            capture_exception(e)
        else:
            print(e)
    # # migrate opportunity records to django

    """
    to do using threading
    """
    # migrate_functions = [opportunity_migrate, account_migrate, contact_migrate]
    # threads = []
    # for migrate_function in migrate_functions:
    #     x = threading.Thread(target=migrate_function, args=(con, cur))
    #     threads.append(x)
    #     x.start()
    #
    # for thread in threads:
    #     thread.join()

    # opps = getAllOpps()
    # print(opps)
    # company_account = getAllAccounts()
    # print(company_account)
    # logger.info("Saved image from Flickr")
    print('Done running updates')
