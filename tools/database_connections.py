import pprint
import psycopg2
from simple_salesforce import Salesforce
from decouple import config


# initalize salesforce instance
def init():
    print(f"usersname {config('SF_USERNAME')}")
    print(f"password {config('SF_PASSWORD')}")
    print(f"security_token {config('SF_TOKEN')}")
    sf = Salesforce(username=config('SF_USERNAME'), password=config('SF_PASSWORD'),
                    security_token=config('SF_TOKEN'), organizationId='00DE0000000Iuwz')
    return sf


def dbinit():
    con = None
    try:
        con = psycopg2.connect(
            f"host={config('DB_HOST')} dbname={config('DB_NAME')} user={config('DB_USER')} password={config('DB_PWD')} port={config('DB_PORT')}")
        return con
    except psycopg2.Error as e:
        print("error: {}".format(e))
        if con:
            con.close()

