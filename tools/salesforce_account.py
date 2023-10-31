import sys
from datetime import datetime

from decouple import config
from django.utils.text import slugify
from sentry_sdk import capture_exception

from app.api.projects.models import CompanyAccount, Opportunity

update_existing_records = True


def getAllAccounts(sf):
    q = "SELECT Id, Name, BillingAddress, Phone, Fax, Website, Industry, Market_Working_Region__c, planroomlink__c, Opportunity_Source__c, \
        Opportunity_Source_Stage_Type__c, No_Planroom_Confirmed__c, planroomopptype__c, No_itb_sending_confirmed__c, Twitter__c, FaceBook_Page__c, LinkedIn__c, Youtube__c, \
        Prequalification_application__c, Confirmed_no_prequal_application__c, No_of_Contacts_with_Email_Address__c, Open_Opportunities__c, Signatory_to_union__c, \
        Prevailing_Wage__c, Internal_cleaning_reason__c, ENR_Top_Contractors_1_100__c, CreatedDate, LastModifiedDate, \
        BillingStreet, BillingCountry, BillingPostalCode, BillingState, BillingCity, IntelconstructStatus__c, \
        Multiple_Officestext__c,Prequal_application_submit_instruction__c, Instagram__c, French_speaking__c,Contact_HTML_Email_Count__c, \
        Organizational_score__c, Average_opportunity_size__c,Founded__c, Linkedin_Headcount__c, " \
        "Facebook_followers__c, Instagram_followers__c, Twitter_followers__c, Youtube_subscribers__c, " \
        "NAICS_code__c, Sic,LinkedIn_followers__c, Top_overall_contact__c, Top_Estimating__c, top_project_manager__c," \
        "Top_Superintendent__c, Top_Human_resource__c,Number_of_offices__c, Twitter_Bio__c,Youtube_Bio__c, Facebook_Bio__c, " \
        "Instagram_Bio__c, LinkedIn_Bio__c, Logo__c,Intelconstruct_URL__c, Intelconstruct_Company_ID__c, geopointe__Geocode__r.geopointe__Longitude__c," \
        "geopointe__Geocode__r.geopointe__Latitude__c,Top_C_Level__c, All_Opportunities__c,Organizational_Tier__c,Social_Network_Tier__c\
        FROM Account \
        WHERE Industry in ('Canada Construction','Construction','United Kingdom Construction')"
    # " AND  geopointe__Geocode__r.geopointe__Longitude__c != NULL AND geopointe__Geocode__r.geopointe__Latitude__c!=NULL"

    account = sf.query_all(q)
    # print(account)
    records = account['records']

    return records


def getAccount(Id, sf):
    q = "SELECT Id, Name, BillingAddress, Phone, Fax, Website, Industry, Market_Working_Region__c, planroomlink__c, Opportunity_Source__c, \
        Opportunity_Source_Stage_Type__c, No_Planroom_Confirmed__c, planroomopptype__c, No_itb_sending_confirmed__c, Twitter__c, FaceBook_Page__c, LinkedIn__c, Youtube__c, \
        Prequalification_application__c, Confirmed_no_prequal_application__c, No_of_Contacts_with_Email_Address__c, Open_Opportunities__c, Signatory_to_union__c, \
        Prevailing_Wage__c, Internal_cleaning_reason__c, ENR_Top_Contractors_1_100__c, CreatedDate, LastModifiedDate,  \
        BillingStreet, BillingCountry, BillingPostalCode, BillingState, BillingCity  FROM Account \
        WHERE  Id = '" + Id + "' AND Industry in ('Canada Construction','Construction','United Kingdom Construction','Out of Business Construction') LIMIT 1"

    account = sf.query_all(q)
    records = account['records']

    return records


def print_psycopg2_exception(err):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print("\npsycopg2 ERROR:", err, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", err.diag)

    # print the pgcode and pgerror exceptions
    print("pgerror:", err.pgerror)
    print("pgcode:", err.pgcode, "\n")


def account_migrate(con, cur, sf):
    # get all opportunity
    try:
        accounts = getAllAccounts(sf)

        # Make dates readble and clean up project status names
        # opps = humanReadableFields(opps)

        # test if table exist
        cur.execute("select exists(select * from information_schema.tables where table_name=%s)",
                    ('projects_companyaccount',))
        if cur.fetchone()[0]:
            print("table 'projects_companyaccount' exists")
        else:
            print("table 'projects_companyaccount' does not exists")
            raise Exception("Create Migration for CompanyAccount Model ")

        deleted_companies = CompanyAccount.objects.exclude(
            account_id__in=[account['Id'] for account in accounts])
        for deleted_company in deleted_companies:
            Opportunity.objects.filter(company_account_id=deleted_company.account_id).delete()
        deleted_companies.delete()

        for account in accounts:
            cur.execute(
                "SELECT account_id, last_modified_date, multiple_offices_text,slug, social_network_tier FROM projects_companyaccount WHERE account_id =%s",
                (account['Id'],))
            row = cur.fetchone()

            lastmodifiedtime = datetime.strptime(account['LastModifiedDate'], '%Y-%m-%dT%H:%M:%S.000+0000')
            lmt = lastmodifiedtime.replace(tzinfo=None)

            if account['BillingAddress'] is not None:
                account['BillingAddress'] = account['BillingAddress']['street']

            if account['IntelconstructStatus__c'] is None or '':
                account['IntelconstructStatus__c'] = 'A'

            if row == None:
                print("inserting account {}".format(account['Id']))
                # query = """
                sub_sr_id = account['Id'][-7:]
                slug = slugify(f"{account['Name']}-{sub_sr_id}")
                is_archive = False
                intelconstruct_url = f"https://app.ganarpro.com/general-contractor-intelligence/company-profiles/{slug}"
                cur.execute(
                    """
                     INSERT INTO projects_companyaccount (
                     account_id, name, billing_address, phone, fax, website, industry,
                     market_working_region, planroom_link, opportunity_source, opportunity_source_stage_type, no_planroom_confirmed,
                     planroom_opptype, no_itb_sending_confirmed, twitter, facebook_page, linkedin, youtube, prequalification_application,
                     confirmed_no_prequal_application, no_of_contacts_with_email_address, open_opportunities, signatory_to_union,
                     prevailing_wage, internal_cleaning_reason, enr_top_contractors_1_100, created_date,last_modified_date,slug,
                     billing_street, billing_country,billing_postal_code,billing_state,billing_city,status,multiple_offices_text,
                     prequal_application_submit_instruction, instagram,french_speaking, contact_html_email_count,
                     organizational_score, average_project_size, founded, linkedin_head_count,
                     facebook_followers, instagram_followers, twitter_followers,youtube_subscribers, naics_code, sic,
                     linked_in_followers, top_overall_contact, top_estimating,top_project_manager, top_superintendent,
                     top_human_resource, number_of_offices, twitter_bio, youtube_bio, facebook_bio, instagram_bio, 
                     linked_in_bio, logo, intelconstruct_url, intelconstruct_company_id, top_c_level, all_opportunities, is_archive,
                     social_network_tier,organizational_tier
                     )


                     VALUES (
                         %s, %s, %s, %s, %s, %s,
                         %s, %s, %s, %s, %s, %s,
                         %s, %s, %s, %s, %s, %s,
                         %s, %s, %s, %s, %s, %s,
                         %s, %s,%s, %s, %s, %s,
                         %s, %s, %s, %s,%s, %s,
                         %s, %s, %s, %s, %s, %s,
                         %s, %s, %s, %s, %s, %s,
                         %s, %s, %s, %s, %s, %s,
                         %s,%s, %s, %s, %s, %s,
                         %s, %s, %s, %s, %s,
                          %s, %s, %s, %s, %s
                     )
                     """,
                    (
                        account['Id'],
                        account['Name'],
                        account['BillingAddress'],
                        account['Phone'],
                        account['Fax'],
                        account['Website'],
                        account['Industry'],
                        account['Market_Working_Region__c'],
                        account['planroomlink__c'],
                        account['Opportunity_Source__c'],
                        account['Opportunity_Source_Stage_Type__c'],
                        account['No_Planroom_Confirmed__c'],
                        account['planroomopptype__c'],
                        account['No_itb_sending_confirmed__c'],
                        account['Twitter__c'],
                        account['FaceBook_Page__c'],
                        account['LinkedIn__c'],
                        account['Youtube__c'],
                        account['Prequalification_application__c'],
                        account['Confirmed_no_prequal_application__c'],
                        account['No_of_Contacts_with_Email_Address__c'],
                        account['Open_Opportunities__c'],
                        account['Signatory_to_union__c'],
                        account['Prevailing_Wage__c'],
                        account['Internal_cleaning_reason__c'],
                        account['ENR_Top_Contractors_1_100__c'],
                        account['CreatedDate'],
                        account['LastModifiedDate'],
                        slug,
                        account['BillingStreet'],
                        account['BillingCountry'],
                        account['BillingPostalCode'],
                        account['BillingState'],
                        account['BillingCity'],
                        account['IntelconstructStatus__c'],
                        account['Multiple_Officestext__c'],
                        account['Prequal_application_submit_instruction__c'],
                        account['Instagram__c'],
                        account['French_speaking__c'],
                        account['Contact_HTML_Email_Count__c'],
                        account['Organizational_score__c'],
                        account['Average_opportunity_size__c'],
                        account['Founded__c'],
                        account['Linkedin_Headcount__c'],
                        account['Facebook_followers__c'],
                        account['Instagram_followers__c'],
                        account['Twitter_followers__c'],
                        account['Youtube_subscribers__c'],
                        account['NAICS_code__c'],
                        account['Sic'],
                        account['LinkedIn_followers__c'],
                        account['Top_overall_contact__c'],
                        account['Top_Estimating__c'],
                        account['top_project_manager__c'],
                        account['Top_Superintendent__c'],
                        account['Top_Human_resource__c'],
                        account['Number_of_offices__c'],
                        account['Twitter_Bio__c'],
                        account['Youtube_Bio__c'],
                        account['Facebook_Bio__c'],
                        account['Instagram_Bio__c'],
                        account['LinkedIn_Bio__c'],
                        account['Logo__c'],
                        intelconstruct_url,
                        account['Id'],
                        account['Top_C_Level__c'],
                        account['All_Opportunities__c'],
                        is_archive,
                        account['Organizational_Tier__c'],
                        account['Social_Network_Tier__c']

                    ))
                con.commit()



            elif row[1].replace(tzinfo=None) < lmt or row[4] is None:
                print("account ID {} will be updated".format(account['Id']))
                slug = row[3]
                intelconstruct_url = f"https://app.ganarpro.com/general-contractor-intelligence/company-profiles/{slug}"

                cur.execute(
                    """
                     UPDATE projects_companyaccount SET name = %s, billing_address = %s, phone = %s, fax = %s, website = %s, industry = %s,
                     market_working_region = %s, planroom_link = %s, opportunity_source = %s, opportunity_source_stage_type = %s, no_planroom_confirmed = %s,
                     planroom_opptype = %s, no_itb_sending_confirmed = %s, twitter = %s, facebook_page = %s, linkedin = %s, youtube = %s,
                     prequalification_application = %s, confirmed_no_prequal_application = %s, no_of_contacts_with_email_address = %s, open_opportunities = %s, signatory_to_union = %s,
                     prevailing_wage = %s, internal_cleaning_reason = %s, enr_top_contractors_1_100 = %s, created_date = %s,
                     last_modified_date = %s, billing_street = %s, billing_country = %s, billing_postal_code = %s,
                     billing_state = %s, billing_city = %s , status = %s, multiple_offices_text = %s,
                      prequal_application_submit_instruction = %s, instagram = %s, french_speaking = %s,
                      contact_html_email_count=%s, organizational_score=%s, average_project_size=%s, founded=%s,
                      linkedin_head_count=%s, facebook_followers=%s, instagram_followers=%s, twitter_followers=%s,
                        youtube_subscribers=%s, naics_code=%s, sic=%s, linked_in_followers=%s,
                        top_overall_contact=%s,top_estimating=%s, top_project_manager=%s,
                         top_superintendent=%s, top_human_resource=%s, number_of_offices=%s,
                          twitter_bio=%s, youtube_bio=%s, facebook_bio=%s, instagram_bio=%s, linked_in_bio=%s, logo=%s,
                           intelconstruct_url=%s, intelconstruct_company_id=%s, latitude=%s, all_opportunities=%s,
                           social_network_tier=%s, organizational_tier=%s
                           WHERE account_id = %s;
                     """,
                    (

                        account['Name'],
                        account['BillingAddress'],
                        account['Phone'],
                        account['Fax'],
                        account['Website'],
                        account['Industry'],
                        account['Market_Working_Region__c'],
                        account['planroomlink__c'],
                        account['Opportunity_Source__c'],
                        account['Opportunity_Source_Stage_Type__c'],
                        account['No_Planroom_Confirmed__c'],
                        account['planroomopptype__c'],
                        account['No_itb_sending_confirmed__c'],
                        account['Twitter__c'],
                        account['FaceBook_Page__c'],
                        account['LinkedIn__c'],
                        account['Youtube__c'],
                        account['Prequalification_application__c'],
                        account['Confirmed_no_prequal_application__c'],
                        account['No_of_Contacts_with_Email_Address__c'],
                        account['Open_Opportunities__c'],
                        account['Signatory_to_union__c'],
                        account['Prevailing_Wage__c'],
                        account['Internal_cleaning_reason__c'],
                        account['ENR_Top_Contractors_1_100__c'],
                        account['CreatedDate'],
                        account['LastModifiedDate'],
                        account['BillingStreet'],
                        account['BillingCountry'],
                        account['BillingPostalCode'],
                        account['BillingState'],
                        account['BillingCity'],
                        account['IntelconstructStatus__c'],
                        account['Multiple_Officestext__c'],
                        account['Prequal_application_submit_instruction__c'],
                        account['Instagram__c'],
                        account['French_speaking__c'],
                        account['Contact_HTML_Email_Count__c'],
                        account['Organizational_score__c'],
                        account['Average_opportunity_size__c'],
                        account['Founded__c'],
                        account['Linkedin_Headcount__c'],
                        account['Facebook_followers__c'],
                        account['Instagram_followers__c'],
                        account['Twitter_followers__c'],
                        account['Youtube_subscribers__c'],
                        account['NAICS_code__c'],
                        account['Sic'],
                        account['LinkedIn_followers__c'],
                        account['Top_overall_contact__c'],
                        account['Top_Estimating__c'],
                        account['top_project_manager__c'],
                        account['Top_Superintendent__c'],
                        account['Top_Human_resource__c'],
                        account['Number_of_offices__c'],
                        account['Twitter_Bio__c'],
                        account['Youtube_Bio__c'],
                        account['Facebook_Bio__c'],
                        account['Instagram_Bio__c'],
                        account['LinkedIn_Bio__c'],
                        account['Logo__c'],
                        intelconstruct_url,
                        account['Id'],
                        account['Top_C_Level__c'],
                        account['All_Opportunities__c'],
                        account['Organizational_Tier__c'],
                        account['Social_Network_Tier__c'],
                        account['Id']
                    ))
                con.commit()
    except Exception as e:
        if not config('DEBUG', '', cast=bool):
            capture_exception(e)
        else:
            print(e)
