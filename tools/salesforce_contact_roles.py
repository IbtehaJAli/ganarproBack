import sys
import os

from decouple import config
from salesforce_functions import expose_django_settings
from datetime import datetime

from django.utils.text import slugify
from sentry_sdk import capture_exception


from app.api.projects.models import ContactRole, Opportunity

expose_django_settings()
def getContactRoles(sf):


    q = "SELECT OpportunityId__c,Id,ContactId__c, ContactId__r.Name,Account_Name__r.Name, Account_Name__r.Id, Email__c, Phone__c, " \
        "Role__c, CreatedDate, LastModifiedDate FROM Contact_Role__c" \
        " WHERE Role__C != 'Final clean scheduler' AND OpportunityId__c !='' AND ContactId__r.Name !='' AND Account_Name__r.Name!='' "

    result = sf.query_all(q)
    records = result['records']
    return records


def contactrole_migrate(con, cur, sf):
    # get all opportunity
    try:
        contactroles = getContactRoles(sf)

        # Make dates readble and clean up project status names
        # opps = humanReadableFields(opps)

        # test if table exist
        cur.execute("select exists(select * from information_schema.tables where table_name=%s)",
                    ('projects_contactrole',))
        if cur.fetchone()[0]:
            print("table 'projects_contactrole' exists")
        else:
            print("table 'projects_contactrole' does not exists")
            raise Exception("Create Migration for Contact Model ")

        # Clean up opportunties that have been deleted in salesforce.
        # create list of newly query salesforce opportunties to test against
        cur.execute("SELECT contact_role_id,name FROM projects_contactrole")

        records = cur.fetchall()

        ContactRole.objects.exclude(contact_role_id__in=[contactrole['Id'] for contactrole in contactroles]).delete()

        for contactrole in contactroles:

            # test if opportuntity exists already
            cur.execute("SELECT contact_role_id, modified, opportunityid_id FROM projects_contactrole WHERE contact_role_id =%s",
                        (contactrole['Id'],))
            row = cur.fetchone()
            # print(f"row{row}")
            lastmodifiedtime = datetime.strptime(contactrole['LastModifiedDate'], '%Y-%m-%dT%H:%M:%S.000+0000')
            lmt = lastmodifiedtime.replace(tzinfo=None)

            sub_sr_id = contactrole['Id'][-7:]
            slug = slugify(f"{contactrole['ContactId__r']['Name']}-{sub_sr_id}")
            if row == None:
                print(f"inserting contact role {contactrole['ContactId__r']['Name']}")
                contact_role = ContactRole(
                    contact_role_id= contactrole['Id'],
                    contact_id=contactrole['ContactId__c'],
                    name=contactrole['ContactId__r']['Name'],
                    phone=contactrole['Phone__c'],
                    email=contactrole['Email__c'],
                    role=contactrole['Role__c'],
                    account_id=contactrole['Account_Name__r']['Id'],
                    account_name=contactrole['Account_Name__r']['Name'],
                    created=contactrole['CreatedDate'],
                    modified=contactrole['LastModifiedDate'],
                    opportunity_id=contactrole['OpportunityId__c'],
                    slug=slug
                )
                try:
                    opportunity = Opportunity.objects.get(oppid=contactrole['OpportunityId__c'])
                    contact_role.opportunityid = opportunity
                    print(f"inserting opp  {opportunity.id}  {contact_role.contact_role_id}")
                except Opportunity.DoesNotExist:
                    contact_role.opportunityid = None
                contact_role.save()

            elif row[1].replace(tzinfo=None) < lmt or row[2] is None:
                print(f"updated contact role {contactrole['ContactId__r']['Name']}")
                contact_role = ContactRole.objects.get(contact_role_id=contactrole['Id'])
                contact_role.name = contactrole['ContactId__r']['Name']
                contact_role.contact_id = contactrole['ContactId__c']
                contact_role.phone = contactrole['Phone__c']
                contact_role.email = contactrole['Email__c']
                contact_role.role = contactrole['Role__c']
                contact_role.opportunity_id = contactrole['OpportunityId__c']
                contact_role.account_id = contactrole['Account_Name__r']['Id']
                contact_role.account_name = contactrole['Account_Name__r']['Name']
                contact_role.created = contactrole['CreatedDate']
                contact_role.modified = contactrole['LastModifiedDate']
                contact_role.slug = slug
                try:
                    opportunity = Opportunity.objects.get(oppid=contactrole['OpportunityId__c'])
                    contact_role.opportunityid = opportunity
                    print(f"inserting opp  {opportunity.id}  {contact_role.contact_role_id}")
                except Opportunity.DoesNotExist:
                    contact_role.opportunityid = None
                contact_role.save()
    except Exception as e:
        if not config('DEBUG', '', cast=bool):
            capture_exception(e)
        else:
            print(e)

