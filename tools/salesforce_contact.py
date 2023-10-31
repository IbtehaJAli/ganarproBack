from datetime import datetime
from decouple import config
from django.utils.text import slugify

from salesforce_functions import fixDate, single_contact

# update_existing_records = True
from sentry_sdk import capture_exception

from app.api.projects.models import Contact


def getContacts(sf):

    q = "SELECT Id, Name,Phone, Email, Title, key_Estimating_project_stage_knowledge__c, key_compliance__c, \
          Accounting__c, Hiring_person__c, Confirmed_no_email__c, No_bid_knowledge__c, No_longer_employed__c, \
        Account.Id, CreatedDate, LastModifiedDate, IntelconstructStatus__c, HTML_Email_Count__c FROM Contact" \
        " WHERE Account.Industry in ('Canada Construction','Construction','United Kingdom Construction')" \
        " AND No_longer_employed__c = NULL AND Email  != NULL"

    result = sf.query_all(q)
    records = result['records']

    return records

def contact_migrate(con, cur, sf):
    # get all opportunity
    try:
        contacts = getContacts(sf)

        # Make dates readble and clean up project status names
        # opps = humanReadableFields(opps)

        # test if table exist
        cur.execute("select exists(select * from information_schema.tables where table_name=%s)",
                    ('projects_contact',))
        if cur.fetchone()[0]:
            print("table 'projects_contact' exists")
        else:
            print("table 'projects_contact' does not exists")
            raise Exception("Create Migration for Contact Model ")

        # Clean up opportunties that have been deleted in salesforce.
        # create list of newly query salesforce opportunties to test against
        # new_id_list = []
        # for contact in contacts:
        #     new_id_list.append(contact['Id'])

        # cur.execute("SELECT contact_id FROM projects_contact")
        # records = cur.fetchall()
        # for record in records:
        #     if record[0] not in new_id_list:
        #         print("Deleting no longer existing contact record: {}".format(record[0]))
        #         cur.execute("DELETE FROM projects_contact WHERE contact_id =%s", (record[0],))
        Contact.objects.exclude(
            contact_id__in=[contact['Id'] for contact in contacts]).delete()

        for contact in contacts:

            # test if opportuntity exists already
            cur.execute("SELECT contact_id, last_modified_date FROM projects_contact WHERE contact_id =%s",
                        (contact['Id'],))
            row = cur.fetchone()
            lastmodifiedtime = datetime.strptime(contact['LastModifiedDate'], '%Y-%m-%dT%H:%M:%S.000+0000')
            lmt = lastmodifiedtime.replace(tzinfo=None)

            region_name = single_contact(contact['Phone'])

            if contact['IntelconstructStatus__c'] is None or '':
                contact['IntelconstructStatus__c'] = 'A'

            if row == None:
                print(f"inserting contact {contact['Id']} region {region_name}" )
                # query = """
                sub_sr_id = contact['Id'][-7:]
                slug = slugify(f"{contact['Name']}-{sub_sr_id}")
                cur.execute(
                    """
                     INSERT INTO projects_contact (contact_id, name, phone, email, title, key_estimating_project_stage_knowledge,
                     key_compliance, accounting, hiring_person, confirmed_no_email, no_bid_knowledge, no_longer_employed,
                     created_date, last_modified_date, company_account_id, slug, region, status, html_email_count
                     )


                     VALUES (
                         %s, %s, %s, %s, %s, %s,
                         %s, %s, %s, %s, %s, %s,
                         %s, %s,%s, %s, %s, %s, %s
                     );
                     """,
                    (
                        contact['Id'],
                        contact['Name'],
                        contact['Phone'],
                        contact['Email'],
                        contact['Title'],
                        contact['key_Estimating_project_stage_knowledge__c'],
                        contact['key_compliance__c'],
                        contact['Accounting__c'],
                        contact['Hiring_person__c'],
                        contact['Confirmed_no_email__c'],
                        contact['No_bid_knowledge__c'],
                        contact['No_longer_employed__c'],
                        contact['CreatedDate'],
                        contact['LastModifiedDate'],
                        contact['Account']['Id'],
                        slug,
                        region_name,# update region for contact
                        contact['IntelconstructStatus__c'],
                        contact['HTML_Email_Count__c'],

                    ))
                con.commit()

            elif row[1].replace(tzinfo=None) < lmt:
                print(f"contact ID {contact['Id']} will be updated region {region_name}")

                cur.execute(
                    """
                     UPDATE projects_contact SET name = %s, phone = %s, email = %s, title = %s, key_estimating_project_stage_knowledge = %s, key_compliance = %s,
                     accounting = %s, hiring_person = %s, confirmed_no_email = %s, no_bid_knowledge = %s, no_longer_employed = %s,
                     created_date = %s, last_modified_date = %s, company_account_id= %s, region = %s , status = %s, html_email_count = %s WHERE contact_id = %s;
                     """,
                    (
                        contact['Name'],
                        contact['Phone'],
                        contact['Email'],
                        contact['Title'],
                        contact['key_Estimating_project_stage_knowledge__c'],
                        contact['key_compliance__c'],
                        contact['Accounting__c'],
                        contact['Hiring_person__c'],
                        contact['Confirmed_no_email__c'],
                        contact['No_bid_knowledge__c'],
                        contact['No_longer_employed__c'],
                        contact['CreatedDate'],
                        contact['LastModifiedDate'],
                        contact['Account']['Id'],
                        region_name, # update region for contact
                        contact['IntelconstructStatus__c'],
                        contact['HTML_Email_Count__c'],
                        contact['Id'],
                    ))
                con.commit()
    except Exception as e:
        if not config('DEBUG', '', cast=bool):
            capture_exception(e)
        else:
            print(e)
