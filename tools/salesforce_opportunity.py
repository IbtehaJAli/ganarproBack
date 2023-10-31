import django
from decouple import config
from django.contrib.gis.geos import Point
from django.utils.text import slugify
from salesforce_functions import fixDate, fixStatusUpdateDate, single_opportunity, expose_django_settings
from datetime import datetime
import re
from sentry_sdk import capture_exception

# expose_django_settings()

from app.settings.local import DATABASES, INSTALLED_APPS
# from app.api.proposal.models import Proposal
from app.api.projects.models import Opportunity
pattern = re.compile('[\W_]+')
update_existing_records = True
types = {
    'a0ME00000077CEOMA2': 'Military',
    'a0ME00000077CEdMAM': 'Police-Fire Station',
    'a0ME00000077CEYMA2': 'Recreation Center',
    'a0ME00000077CEiMAM': 'Bank',
    'a0ME000000JTv8MMAT': 'Data center',
    'a0ME0000003ZeYdMAK': 'Worship',
    'a0ME00000035IToMAM': 'Theatre',
    'a0ME0000009HUGjMAO': 'Athletic',
    'a0ME0000003YRLGMA4': 'Medical-Dental',
    'a0ME0000003YTy8MAG': 'Fitness',
    'a0ME0000003WJcYMAW': 'Gas Station',
    'a0ME0000003YT6RMAW': 'Auto Office-Bay',
    'a0ME0000003YTyDMAW': 'Grocery',
    'a0ME0000003YlycMAC': 'Library',
    'a0ME0000004afxNMAQ': 'Car dealership',
    'a0ME0000004afxDMAQ': 'Industrial',
    'a0ME00000034z9NMAQ': 'Restaurant',
    'a0ME00000034wTPMAY': 'Retail',
    'a0ME00000034z9IMAQ': 'Multi-family residential',
    'a0ME00000034z9SMAQ': 'Interior tenant fit out',
    'a0ME00000034z9DMAQ': 'Education',
    'a0ME0000003ZtY1MAK': 'WWTP',
    'a0ME0000003ZeYi': 'Senior living Retirement',
    'a0ME0000003ZeYiMAK': 'Senior living Retirement',
    'a0M2R00000aUioU': 'Community / Public',
    'a0M2R00000aUioUUAS': 'Community / Public',
    'a0M2R00000aUj1Z': 'Mixed Use',
    'a0M2R00000aUj1ZUAS': 'Mixed Use',
    'a0M2R00000aUioe': 'Parking',
    'a0M2R00000aUioeUAC': 'Parking',
    'a0M2R00000aUioZ': 'Corporate',
    'a0M2R00000aUioZUAS': 'Corporate',
    'a0M2R00000aUioU': 'Community / Public',
    'a0M2R00000aUjvl': 'Airport',
    'a0M2R00000aUjvlUAC': 'Airport',
    'a0M2R00000aUksB': 'Renovation Addition',
    'a0M2R00000aUksBUAS': 'Renovation Addition',
    'a0ME0000004afx3': 'Zoo',
    'a0ME0000004afx3MAA': 'Zoo',
    'a0ME0000007gRfk': 'Window clean',
    'a0ME0000007gRfkMAE': 'Window Clean',
    'a0ME00000077CGy': 'Transit station',
    'a0ME00000077CGyMAM': 'Transit station',
    'a0ME0000004afwo': 'Residential Home',
    'a0ME0000004afwoMAA': 'Residential Home',
    'a0ME0000007Aky7': 'Pressure Wash',
    'a0ME0000007gzfY': 'Job trailer',
    'a0ME0000007gzfYMAQ': 'Job trailer',
    'a0ME0000007gRg9': 'Flooring service',
    'a0ME0000007gRfz': 'Duct clean',
    'a0ME00000079APi': 'Clean Room',
    'a0ME00000077CEE': 'Bathroom cleaning',
    'a0ME00000077CDuMAM': 'Miscellaneous',
    'a0ME0000007gRfuMAE': 'Carpet clean',
    'a0ME0000007Aky7MAC': 'Pressure Wash',
    'a0ME0000007gRg9MAE': 'Flooring service'
}

STATES = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
    'AB': 'Alberta',
    'BC': 'British Columbia',
    'MB': 'Manitoba',
    'NS': 'Nova Scotia',
    'NT': 'Northwest Territories',
    'NU': 'Nunavut',
    'ON': 'Ontario',
    'QC': 'Quebec',
    'NL': 'Newfoundland',
    'SK': 'Saskatchewan',
    'ENG': 'England',
    'NIR': 'Northern Ireland',
    'SCT': 'Scotland',
    'WAL': 'Wales',
    'State': 'None',
    'CN': 'Canada',
    'NB': 'New Brunswick',

}


def humanReadableFields(records):
    for r in records:
        if r['StageName'] == 'ProjectinProgress Decision Maker ID' or r['StageName'] == 'Project in progress' or r[
            'StageName'] == 'Negotiations':
            r['StageName'] = 'Broke Ground'
        else:
            r['StageName'] = 'Pre-construction'
        date = fixDate(r['LastModifiedDate'])
        r['LastModifiedDateString'] = date

        if r['Project_Type__c']:
            r['Project_Type__c'] = types[r['Project_Type__c']]
        # Change state/province initial to full name
        if r['State__r']['Name'] in STATES:
            r['State__r']['Name'] = STATES[r['State__r']['Name']]

        if r['Status_update_1_date__c']:
            r['Status_update_1_date__c'] = fixStatusUpdateDate(r['Status_update_1_date__c'])

        if r['Status_update_2_date__c']:
            r['Status_update_2_date__c'] = fixStatusUpdateDate(r['Status_update_2_date__c'])

        if r['BidDueDate__c']:
            r['BidDueDate__c'] = fixStatusUpdateDate(r['BidDueDate__c'])

    return records


def getAllOpps(sf):
    q = "SELECT Id, Name, streetaddressopp__c, city__c, State__r.Name, Zip_code__c, Account.Name, Description, Opportunity_package__c, \
        Plans_Drawings__c, CreatedDate, LastModifiedDate, When__c, BidDueDate__c, Units__c, Primary_Contact__c,Primary_Contact_Phone__c,Primary_Contact_Email__c," \
        "SF_Size__c, StageName, Project_type__c, Site_Contact__c, Site_Contact_Phone__c, Site_Contact_Email__c, \
        Send_Partner_Details__c, CloseDate, pipdcmkr_approval__c, Account_Formula_Name__c, Account_Billing_Address__c, Account_Phone__c, \
        Account_Website__c, Account_Prequalification_application__c, Account_LinkedIn__c, Account_Facebook_Page__c,Account_Twitter__c, \
        Status_update_1__c, Status_update_1_date__c, Status_update_2__c, Status_update_2_date__c, Status_update_3__c, Status_update_3_date__c, \
        Status_update_4__c, Status_update_4_date__c,Status_contact_role_update_5__c, Status_contact_role_update_5_date__c, Hot_lead_Trade_Scope__c, Negative_Scope__c, Account.Id, " \
        "Project_completion__c,union__c, Davis_Bacon_Prevailing_Wage_details__c,geopointe__Geocode__r.geopointe__Longitude__c, geopointe__Geocode__r.geopointe__Latitude__c, PQ_score__c,\
         Project_Quality_Tier__c, Est_Break_ground_date__c FROM Opportunity WHERE city__c != NULL AND  geopointe__Geocode__r.geopointe__Longitude__c != NULL " \
        "AND geopointe__Geocode__r.geopointe__Latitude__c!=NULL AND State__r.Name != NULL AND  StageName IN  ('Negotiations','Bidding-GC', 'Project in progress', 'ProjectinProgress Decision Maker ID'," \
        " 'Project on Hold', 'Cleaning concierge', 'Awarded', 'Closed', 'Awarded-Failed Contract', 'Closed Complete', 'Closed Not GC', 'Closed') "\
        "AND Account.Industry IN ('Canada Construction','Construction','United Kingdom Construction') " \
        "AND Account.Industry IN ('Canada Construction','Construction','United Kingdom Construction') AND CreatedDate >= 2017-01-01T00:00:00.000+0000 "

    result = sf.query_all(q)
    records = result['records']

    return records


def getOppInfo(id, sf):
    q = "SELECT Id, Name, streetaddressopp__c, city__c, State__r.Name, Zip_code__c, Account.Name, Description, Opportunity_package__c, \
        Plans_Drawings__c, CreatedDate, LastModifiedDate, When__c, BidDueDate__c, Units__c, SF_Size__c, StageName, Project_type__c, \
        Send_Partner_Details__c, CloseDate, pipdcmkr_approval__c, Account_Formula_Name__c, Account_Billing_Address__c, Account_Phone__c, \
        Account_Website__c, Account_Prequalification_application__c, Account_LinkedIn__c, Account_Facebook_Page__c,Account_Twitter__c, \
        Status_update_1__c, Status_update_1_date__c, Status_update_2__c, Status_update_2_date__c, Status_update_3__c, Status_update_3_date__c, \
        Status_update_4__c, Status_update_4_date__c,Status_contact_role_update_5__c, Status_contact_role_update_5_date__c, Hot_lead_Trade_Scope__c, Negative_Scope__c, Account.Id, " \
        "Project_completion__c,union__c, Davis_Bacon_Prevailing_Wage_details__c, geopointe__Geocode__r.geopointe__Longitude__c, geopointe__Geocode__r.geopointe__Latitude__c " \
        " FROM Opportunity WHERE Id = '" + id + "'"

    result = sf.query_all(q)
    record = result['records']

    return record


def opportunity_migrate(con, cur, sf):
    # Clean up opportunties that have been deleted in salesforce.
    # create list of newly query salesforce opportunties to test against
    # new_id_list = []
    # for opp in opps:
    #     new_id_list.append(opp['Id'])

    # cur.execute("SELECT oppid FROM search_opportunity")
    # records = cur.fetchall()
    # for record in records:
    #     if record[0] not in new_id_list:
    #         print("Deleting no longer existing opportunity: {}".format(record[0]))
    #         cur.execute("DELETE FROM search_opportunity WHERE oppid =%s", (record[0],))

    # cur.execute("SELECT oppid,name FROM search_opportunity WHERE company_account_id IS NULL")
    # opportunity_without_id = [r[0] for r in cur.fetchall()] # update exiting opportunity record without company_account_id
    #
    #
    # for opp in opps:
    #     if opp['Id'] in opportunity_without_id:
    #         print(f"updating Opportunity Id {opp['Id']} without Account Id")
    #         cur.execute("UPDATE search_opportunity SET company_account_id=%s  WHERE oppid =%s", (opp['Account']['Id'], opp['Id']))
    try:
        opps = getAllOpps(sf)

        deleted_opportunities = Opportunity.objects.exclude(
            oppid__in=[opp['Id'] for opp in opps])
        deleted_opportunities.delete()

        count = 0
        for opp in opps:
            # test if opportuntity exists already
            try:
                cur.execute(
                    "SELECT oppid, last_modified_date,status, name, est_break_ground_date, point FROM projects_opportunity WHERE oppid =%s",
                    (opp['Id'],))
                row = cur.fetchone()
            except Exception as e:
                print(e)

            d = opp

            # Make dates human readable
            status = 'A'
            if d['StageName'] == 'ProjectinProgress Decision Maker ID' or d['StageName'] == 'Project in progress' or d[
                'StageName'] == 'Negotiations' or d['StageName'] == 'Project on Hold':
                d['StageName'] = 'Work in progress'
                status = 'A'
            elif d['StageName'] == 'Bidding-GC':
                d['StageName'] = 'Pre-construction'
                status = 'A'
            elif d['StageName'] == 'Cleaning concierge':
                d['StageName'] = '90% contracts purchased'
                status = 'A'
            elif d['StageName'] == 'Awarded' or d['StageName'] == 'Closed' or d[
                'StageName'] == 'Awarded-Failed Contract' \
                    or d['StageName'] == 'Contract' or d['StageName'] == 'Closed Complete':
                d['StageName'] = 'Complete'
                status = 'NA'
            elif d['StageName'] == 'Closed Not GC':
                d['StageName'] = 'GC not awarded'
                status = 'NA'
            elif d['StageName'] == 'Duplicate delete':
                status = 'NA'
            else:
                status = 'None'

            if d['Project_Type__c']:
                d['Project_Type__c'] = types[d['Project_Type__c']]
            try:

                if d['State__r']['Name'] in STATES:
                    d['State'] = STATES[d['State__r']['Name']]
            except Exception as e:
                d['State'] = 'None'

                # Make all the dates humans readable
            mdate = fixDate(d['LastModifiedDate'])
            d['LastModifiedDate_simple'] = mdate

            # Get time object from lastModifiedDate
            lastmodifiedtime = datetime.strptime(d['LastModifiedDate'], '%Y-%m-%dT%H:%M:%S.000+0000')
            lmt = lastmodifiedtime.replace(tzinfo=None)

            #set Primary Contact keys to None if not available
            primary_contact_name = None
            primary_contact_phone = None
            primary_contact_email = None

            if d['Primary_Contact__c']:
                primary_contact_name = d['Primary_Contact__c']
            if d['Primary_Contact_Phone__c']:
                primary_contact_phone = d['Primary_Contact_Phone__c']
            if d['Primary_Contact_Email__c']:
                primary_contact_email = d['Primary_Contact_Email__c']

            # Fix other date string for Contact/Status Update Date
            ndate = fixStatusUpdateDate(d['Status_update_1_date__c'])
            d['Status_update_1_date__c'] = ndate

            ndate = fixStatusUpdateDate(d['Status_update_2_date__c'])
            d['Status_update_2_date__c'] = ndate

            ndate = fixStatusUpdateDate(d['Status_update_3_date__c'])
            d['Status_update_3_date__c'] = ndate

            ndate = fixStatusUpdateDate(d['Status_update_4_date__c'])
            d['Status_update_4_date__c'] = ndate

            ndate = fixStatusUpdateDate(d['Status_contact_role_update_5_date__c'])
            d['Status_contact_role_update_5_date__c'] = ndate

            # ndatendate = fixStatusUpdateDate(d['BidDueDate__c'])
            # d['BidDueDate__c'] = ndatendate

            # fix oppos without sf_size
            if d['SF_Size__c'] == None:
                d['SF_Size__c'] = 0

            # fix none values
            # for key in d:
            #     if key == 'BidDueDate__c' or key == 'Project_completion__c' or key == 'PQ_score__c' or :
            #         continue
            #     if d[key] == None:
            #         d[key] = 'None'

            # Generate URL slug
            # d['url_slug'] = pattern.sub('-', d['Name'])
            country_name = single_opportunity(d['State__r']['Name'])
            opp_id = opp['Id'][-7:]
            d['url_slug'] = slugify(f"{d['Name']}-{opp_id}")
            if row == None:


                print(
                    f"Opportunity ID {opp['Id']} {opp['Name']} will be created")
                opportunity = Opportunity(
                    oppid=opp['Id'],
                    name=d['Name'],
                    address=d['streetaddressopp__c'],
                    city=d['city__c'],
                    state_short=d['State__r']['Name'],
                    state=d['State'],
                    zip_code=d['Zip_code__c'],
                    account_name=d['Account']['Name'],
                    description=d['Description'],
                    opportunity_package=d['Opportunity_package__c'],
                    plan_drawings=d['Plans_Drawings__c'],
                    created_date=d['CreatedDate'],
                    last_modified_date=d['LastModifiedDate'],
                    when_c=d['When__c'],
                    bid_due_date=d['BidDueDate__c'],
                    units=d['Units__c'],
                    sf_size=d['SF_Size__c'],
                    stage_name=d['StageName'],
                    project_type=d['Project_Type__c'],
                    send_partner_details=d['Send_Partner_Details__c'],
                    close_date=d['CloseDate'],
                    pipdcmkr_approval=d['pipdcmkr_approval__c'],
                    account_formula_name=d['Account_Formula_Name__c'],
                    account_billing_address=d['Account_Billing_Address__c'],
                    account_phone=d['Account_Phone__c'],
                    account_website=d['Account_Website__c'],
                    account_prequalification_application=d['Account_Prequalification_application__c'],
                    account_linkedin=d['Account_LinkedIn__c'],
                    account_facebook=d['Account_Facebook_Page__c'],
                    account_twitter=d['Account_Twitter__c'],
                    status_update_1=d['Status_update_1__c'],
                    status_update_1_date=d['Status_update_1_date__c'],
                    status_update_2=d['Status_update_2__c'],
                    status_update_2_date=d['Status_update_2_date__c'],
                    status_update_3=d['Status_update_3__c'],
                    status_update_3_date=d['Status_update_3_date__c'],
                    status_update_4=d['Status_update_4__c'],
                    status_update_4_date=d['Status_update_4_date__c'],
                    last_modified_date_simple=d['LastModifiedDate_simple'],
                    hot_lead_trade_scope=d['Hot_lead_Trade_Scope__c'],
                    url_slug=d['url_slug'],
                    status_update_5=d['Status_contact_role_update_5__c'],
                    status_update_5_date=d['Status_contact_role_update_5_date__c'],
                    negative_scope=d['Negative_Scope__c'],
                    company_account_id=d['Account']['Id'],
                    status=status,
                    country=country_name,  # update opportunity country
                    project_completion=d['Project_completion__c'],
                    laborer_union=d['union__c'],
                    davis_bacon_prevailing_wage_detail=d['Davis_Bacon_Prevailing_Wage_details__c'],
                    primary_contact_name=primary_contact_name,
                    primary_contact_phone=primary_contact_phone,
                    primary_contact_email=primary_contact_email,
                    site_contact_name=d['Site_Contact__c'],
                    site_contact_phone=d['Site_Contact_Phone__c'],
                    site_contact_email=d['Site_Contact_Email__c'],
                    longitude=d['geopointe__Geocode__r']['geopointe__Longitude__c'],
                    latitude=d['geopointe__Geocode__r']['geopointe__Latitude__c'],
                    pq_score=d['PQ_score__c'],
                    project_quality_tier=d['Project_Quality_Tier__c'],
                    est_break_ground_date=d['Est_Break_ground_date__c']
                )
                opportunity.save()
            else:
                # UPDATE
                # for key in d:

                #     print("key: '{}'   value: '{}' ".format(key, d[key]))
                # print('opp[Id]: {}'.format(opp['Id']))
                try:
                    print(
                        f"Opportunity ID {opp['Id']} {opp['Name']} will be updated")
                    opportunity = Opportunity.objects.get(oppid=opp['Id'])
                    opportunity.name = d['Name']
                    opportunity.address = d['streetaddressopp__c']
                    opportunity.city = d['city__c']
                    opportunity.state_short = d['State__r']['Name']
                    opportunity.state = d['State']
                    opportunity.zip_code = d['Zip_code__c']
                    opportunity.account_name = d['Account']['Name']
                    opportunity.description = d['Description']
                    opportunity.opportunity_package = d['Opportunity_package__c']
                    opportunity.plan_drawings = d['Plans_Drawings__c']
                    opportunity.created_date = d['CreatedDate']
                    opportunity.last_modified_date = d['LastModifiedDate']
                    opportunity.when_c = d['When__c']
                    opportunity.bid_due_date = d['BidDueDate__c']
                    opportunity.units = d['Units__c']
                    opportunity.sf_size = int(d['SF_Size__c'])
                    opportunity.stage_name = d['StageName']
                    opportunity.project_type = d['Project_Type__c']
                    opportunity.send_partner_details = d['Send_Partner_Details__c']
                    opportunity.close_date = d['CloseDate']
                    opportunity.pipdcmkr_approval = d['pipdcmkr_approval__c']
                    opportunity.account_formula_name = d['Account_Formula_Name__c']
                    opportunity.account_billing_address = d['Account_Billing_Address__c']
                    opportunity.account_phone = d['Account_Phone__c']
                    opportunity.account_website = d['Account_Website__c']
                    opportunity.account_prequalification_application = d['Account_Prequalification_application__c']
                    opportunity.account_linkedin = d['Account_LinkedIn__c']
                    opportunity.account_facebook = d['Account_Facebook_Page__c']
                    opportunity.account_twitter = d['Account_Twitter__c']
                    opportunity.status_update_1 = d['Status_update_1__c']
                    opportunity.status_update_1_date = d['Status_update_1_date__c']
                    opportunity.status_update_2 = d['Status_update_2__c']
                    opportunity.status_update_2_date = d['Status_update_2_date__c']
                    opportunity.status_update_3 = d['Status_update_3__c']
                    opportunity.status_update_3_date = d['Status_update_3_date__c']
                    opportunity.status_update_4 = d['Status_update_4__c']
                    opportunity.status_update_4_date = d['Status_update_4_date__c']
                    opportunity.last_modified_date_simple = d['LastModifiedDate_simple']
                    opportunity.hot_lead_trade_scope = d['Hot_lead_Trade_Scope__c']
                    opportunity.url_slug = d['url_slug']
                    opportunity.status_update_5 = d['Status_contact_role_update_5__c']
                    opportunity.status_update_5_date = d['Status_contact_role_update_5_date__c']
                    opportunity.negative_scope = d['Negative_Scope__c']
                    opportunity.company_account_id = d['Account']['Id']
                    opportunity.status = status
                    opportunity.country = country_name  # update opportunity country
                    opportunity.project_completion = d['Project_completion__c']
                    opportunity.laborer_union = d['union__c']
                    opportunity.davis_bacon_prevailing_wage_detail = d['Davis_Bacon_Prevailing_Wage_details__c']
                    opportunity.primary_contact_name = primary_contact_name
                    opportunity.primary_contact_phone = primary_contact_phone
                    opportunity.primary_contact_email = primary_contact_email
                    opportunity.site_contact_name = d['Site_Contact__c']
                    opportunity.site_contact_phone = d['Site_Contact_Phone__c']
                    opportunity.site_contact_email = d['Site_Contact_Email__c']
                    opportunity.longitude = d['geopointe__Geocode__r']['geopointe__Longitude__c']
                    opportunity.latitude = d['geopointe__Geocode__r']['geopointe__Latitude__c']
                    opportunity.pq_score = d['PQ_score__c']
                    opportunity.project_quality_tier = d['Project_Quality_Tier__c']
                    opportunity.est_break_ground_date = d['Est_Break_ground_date__c']
                    opportunity.point = Point(float(d['geopointe__Geocode__r']['geopointe__Longitude__c']), float(d['geopointe__Geocode__r']['geopointe__Latitude__c']))
                    opportunity.save()
                except Exception as e:
                    if not config('DEBUG', '', cast=bool):
                        capture_exception(e)
    except Exception as e:
        if not config('DEBUG', '', cast=bool):
            capture_exception(e)
        else:
            print(e)
