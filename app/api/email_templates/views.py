
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.api.authentication.models.user_registration import UserProfile
from app.api.company_details.models import BasicCompany
from app.api.company_details.serializers import BasicCompanySerializer
from app.api.email_templates.helpers import multi_replace_regex
from app.api.email_templates.models import EmailTemplate
from app.api.email_templates.serializers import EmailTemplateSerializers
from app.api.projects.models import Opportunity, CompanyAccount
from app.api.users.serializers import UserProfileSerializer


class EmailTemplateList(generics.ListCreateAPIView):
    serializer_class = EmailTemplateSerializers
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        ids = self.request.query_params.get('ids', None)
        template_ids = []
        if ids:
            for id in ids.split(','):
                if ids != '':
                   template_ids.append(id)
        query_set = EmailTemplate.objects.filter()
        if self.request.query_params.get('type', None):
            query_set = EmailTemplate.objects.filter(type=self.request.query_params['type'])
        if template_ids:
            query_set = EmailTemplate.objects.filter(id__in=template_ids)

        return query_set.order_by('ordering')


class EmailTemplateDetail(generics.RetrieveAPIView):
    """
    Retrieve, update or delete a email instance.
    """
    serializer_class = EmailTemplateSerializers
    permission_classes = (IsAuthenticated,)
    queryset = EmailTemplate.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            get_object_or_404(EmailTemplate, id=kwargs['pk'])
            print('self.request.query_params', self.request.query_params)
            print(f"self.request.query_params {self.request.query_params} args {args} kwargs {kwargs}")


            if self.request.query_params.get('email_type', None):

                template = self.get_mass_email_template(request, kwargs['pk'])
            else:
                if 'project_id' not in self.request.query_params:
                    return Response({"error": '*project_id query params is required'}, status.HTTP_400_BAD_REQUEST)
                elif 'contact_name' not in self.request.query_params:
                    return Response({"error": '*contact_name query params is required'}, status.HTTP_400_BAD_REQUEST)
                elif 'company_id' not in self.request.query_params:
                    return Response({"error": '*company_id query params is required'}, status.HTTP_400_BAD_REQUEST)
                project_id = self.request.query_params['project_id']
                contact_name = self.request.query_params['contact_name']
                company_id = self.request.query_params['company_id']
                template = self.get_email_template(request, kwargs['pk'], project_id, contact_name, company_id)

            if template.get('error') is not None:
                return Response(template, status.HTTP_400_BAD_REQUEST)
            return Response(template)
        except Exception as e:
            return Response({"error": f"Bad request {e}"}, status.HTTP_400_BAD_REQUEST)


    def get_email_template(self, request, temp_id, project_id, contact_name, account_id):
        phone = request.user.profile.phone
        user_firstname = request.user.profile.first_name
        user_lastname = request.user.profile.last_name
        company_name = request.user.profile.company_name
        outbound_email = request.user.profile.outbound_email
        user_email = request.user.email

        user_profile_serializer = UserProfileSerializer(data=UserProfileSerializer(instance=request.user.profile).data)


        if user_profile_serializer.is_valid():
            user_fullname = f"{user_firstname} {user_lastname}"
            template_id = temp_id
            opp_id = project_id
            contact_name = contact_name
            account_id = account_id
            contact_list = contact_name.split(' ')
            first_name = contact_list[0] if len(contact_list) > 0 else contact_list
            email_template = EmailTemplate.objects.filter(pk=template_id).values('title', 'text')
            subject = email_template[0]['title']
            text = email_template[0]['text']
            address = ""
            account_billing_address = ""
            account_name = ""
            user_id = request.user.profile.id
            try:
                basic_company = BasicCompany.objects.only('company_person', 'company_phone',
                                                          'company_name', 'office_address', 'office_city',
                                                          'office_state', 'office_zip',
                                                          'company_specialty').get(user_id=user_id)
            except BasicCompany.DoesNotExist as e:
                return {'error': "Please fill the Company basic information on Prequel Master Key"}




            opp_name = ""
            if opp_id:
                opportunities = Opportunity.objects.filter(id=opp_id) \
                    .values('address', 'account_formula_name', 'account_billing_address', 'name')

                address = opportunities[0]['address'] if opportunities[0]['address'] != 'None' else ''
                account_name = opportunities[0]['account_formula_name']
                account_billing_address = opportunities[0]['account_billing_address']
                opp_name = opportunities[0]['name']
                account_name_list = account_name.split(' ')
                if len(account_name_list) > 0:
                    account_name = account_name_list[0]
            project_types = ''
            company_working_region = ''
            if account_id:
                company = CompanyAccount.objects.get(id=account_id)
                project_types = company.planroom_opptype.replace(';', ', ') if company.planroom_opptype else ""

                company_working_region = company.market_working_region.replace(';',
                                                                               ', ') if company.market_working_region else ""
            # project_types = project_type_list.join(" ")
            # state_name = request.user.account.get_state_display()
            # title_desc = request.user.account.get_title_display()

            replacements = {
                '{CONTACT.FIRSTNAME}': first_name or '{CONTACT.FIRSTNAME}',
                '{USER.COMPANYNAME}': company_name or '{USER.COMPANYNAME}',
                '{PROJECT_NAME}': opp_name or '{PROJECT_NAME}',
                '{USER.FIRSTNAME}': user_firstname or '{USER.FIRSTNAME}',
                '{CONTACT.FIRSTNAME.LASTNAME}': contact_name or '{CONTACT.FIRSTNAME.LASTNAME}',
                '{USER.EMAIL}': user_email or '{USER.EMAIL}',
                '{USER.LASTNAME}': user_lastname or '{USER.LASTNAME}',
                '{USER.PHONE}': phone or '{USER.PHONE}',
                '{USER.FIRSTNAME.LASTNAME}': user_fullname or '{USER.FIRSTNAME.LASTNAME}',
                '{PROJECT.STREET}': address or '{PROJECT.STREET}',
                '{ACCOUNT.COMPANYNAME}': account_name or '{ACCOUNT.COMPANYNAME}',
                '{ACCOUNT.COMPANY.ADDRESS}': account_billing_address or '{ACCOUNT.COMPANY.ADDRESS}',
                '{ACCOUNT.PROJECT.TYPES.BUILT}': project_types or '{ACCOUNT.PROJECT.TYPES.BUILT}',
                '{COMPANY.WORKING.REGION}': company_working_region or '{COMPANY.WORKING.REGION}',
                '{COMPANY.PERSON}':basic_company.company_person or '{COMPANY.PERSON}',
                '{COMPANY.PHONE}': basic_company.company_phone or '{COMPANY.PHONE}',
                '{COMPANY.SPECIALITY}': basic_company.company_specialty or '{COMPANY.SPECIALITY}',
                '{COMPANY.NAME}': basic_company.company_name or '{COMPANY.NAME}',
                '{COMPANY.ADDRESS}': basic_company.office_address or '{COMPANY.ADDRESS}',
                '{COMPANY.CITY}': basic_company.office_city or '{COMPANY.CITY}',
                '{COMPANY.STATE}': basic_company.office_state or '{COMPANY.STATE}',
                '{COMPANY.ZIP}': basic_company.office_zip or '{COMPANY.ZIP}',
                '{OUTBOUND.EMAIL}': outbound_email or '{OUTBOUND.EMAIL}',
            }
            new_text = multi_replace_regex(text, replacements)
            new_subject = multi_replace_regex(subject, replacements)
            return {'subject': new_subject, 'text': new_text}
        return {'error': "User Account Detail is in complete"}


    def get_mass_email_template(self, request, temp_id):
        phone = request.user.profile.phone
        user_firstname = request.user.profile.first_name
        user_lastname = request.user.profile.last_name
        company_name = request.user.profile.company_name
        outbound_email = request.user.profile.outbound_email
        user_email = request.user.email

        user_profile_serializer = UserProfileSerializer(data=UserProfileSerializer(instance=request.user.profile).data)


        if user_profile_serializer.is_valid():
            user_fullname = f"{user_firstname} {user_lastname}"
            template_id = temp_id
            email_template = EmailTemplate.objects.filter(pk=template_id).values('title', 'text')
            subject = email_template[0]['title']
            text = email_template[0]['text']
            address = ""
            account_billing_address = ""
            account_name = ""
            user_id = request.user.profile.id
            try:
                basic_company = BasicCompany.objects.only('company_person', 'company_phone',
                                                          'company_name', 'office_address', 'office_city',
                                                          'office_state', 'office_zip',
                                                          'company_specialty').get(user_id=user_id)
            except BasicCompany.DoesNotExist as e:
                return {'error': "Please fill the Company basic information on Prequel Master Key"}

            # project_types = project_type_list.join(" ")
            # state_name = request.user.account.get_state_display()
            # title_desc = request.user.account.get_title_display()

            replacements = {
                '{USER.COMPANYNAME}': company_name or '{USER.COMPANYNAME}',
                '{USER.FIRSTNAME}': user_firstname or '{USER.FIRSTNAME}',
                '{USER.EMAIL}': user_email or '{USER.EMAIL}',
                '{USER.LASTNAME}': user_lastname or '{USER.LASTNAME}',
                '{USER.PHONE}': phone or '{USER.PHONE}',
                '{USER.FIRSTNAME.LASTNAME}': user_fullname or '{USER.FIRSTNAME.LASTNAME}',
                '{PROJECT.STREET}': address or '{PROJECT.STREET}',
                '{ACCOUNT.COMPANYNAME}': account_name or '{ACCOUNT.COMPANYNAME}',
                '{ACCOUNT.COMPANY.ADDRESS}': account_billing_address or '{ACCOUNT.COMPANY.ADDRESS}',
                '{COMPANY.PERSON}': basic_company.company_person or '{COMPANY.PERSON}',
                '{COMPANY.PHONE}': basic_company.company_phone or '{COMPANY.PHONE}',
                '{COMPANY.SPECIALITY}': basic_company.company_specialty or '{COMPANY.SPECIALITY}',
                '{COMPANY.NAME}': basic_company.company_name or '{COMPANY.NAME}',
                '{COMPANY.ADDRESS}': basic_company.office_address or '{COMPANY.ADDRESS}',
                '{COMPANY.CITY}': basic_company.office_city or '{COMPANY.CITY}',
                '{COMPANY.STATE}': basic_company.office_state or '{COMPANY.STATE}',
                '{COMPANY.ZIP}': basic_company.office_zip or '{COMPANY.ZIP}',
                '{OUTBOUND.EMAIL}': outbound_email or '{OUTBOUND.EMAIL}',
            }
            new_text = multi_replace_regex(text, replacements)
            new_subject = multi_replace_regex(subject, replacements)
            return {'subject': new_subject, 'text': new_text}
        return {'error': "User Account Detail is in complete"}
