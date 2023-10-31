from django.conf import settings
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
from django.http.response import JsonResponse
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from datetime import datetime, timedelta, date, time
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from sendgrid import Mail, SendGridAPIClient

from .helpers import time_sent_and_count_per_project
from .models import UserEmail, EmailManager
from .serializers import SendEmailSerializer
from .service.email_rule_setup.GeneralContractorEmailRule import GeneralContractorEmailRule
from .service.email_rule_setup.ProjectBoardEmailRule import ProjectBoardEmailRule
from ..email_templates.models import EmailTemplate
from ..projects.models import Opportunity, CompanyAccount, ContactRole, Contact


class SendEmailList(generics.ListCreateAPIView):
    """
       List all snippets, or create a new snippet.
       """
    serializer_class = SendEmailSerializer
    queryset = UserEmail.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        time_sent, user_emails_count = time_sent_and_count_per_project(request.user, kwargs['project_id'])
        return Response({'total_email_sent': user_emails_count, "last_email_sent": time_sent, 'data': serializer.data})

    def get_queryset(self):

        return UserEmail.objects.raw("SELECT id,  to_char(time_sent, 'YYYY-MM')time_sent, template_id, opportunity_id,"
                                     f" user_id, account_id='{self.request.user.account.id}', contact_id, email_type, body, subject "
                                     f"FROM search_useremail WHERE email_type='PB'"
                                     f" AND opportunity_id='{self.kwargs['project_id']}' ORDER BY time_sent ")

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        try:
            required_params = ['temp_id', 'subject', 'body']
            for param in required_params:
                if param not in request.data:
                    return Response({"error": f'*{param} query params is required'}, status.HTTP_400_BAD_REQUEST)
            temp_id = request.data['temp_id']

            subject = request.data['subject']
            body = request.data['body']
            if serializer.is_valid(raise_exception=True):
                if request.data.get('email_type', None):
                    project_ids = request.data.get('project_ids', [])
                    email_manager = EmailManager()
                    result = email_manager.send_mass_email(request.user, project_ids, subject, body, temp_id, 'ME')
                    if result.get('error', None):
                        return Response({"error": result['message']}, status.HTTP_400_BAD_REQUEST)

                    return Response({"message": result['message']}, status.HTTP_201_CREATED)
                else:
                    company_id = request.data['company_id']
                    contact_id = request.data.get('contact_id', None)
                    get_object_or_404(Opportunity, id=kwargs['project_id'])
                    get_object_or_404(EmailTemplate, id=request.data['temp_id'])
                    get_object_or_404(CompanyAccount, id=request.data['company_id'])
                    result = self.send_email(request, temp_id, company_id, contact_id, kwargs['project_id'], subject, body)
                    if result.get('error') is not None:
                        return Response(result, status.HTTP_403_FORBIDDEN)

                    return Response(result, status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Bad request {e}"}, status.HTTP_400_BAD_REQUEST)

    def send_email(self, request, temp_id, company_id, contact_id, project_id, subject, body):
        user_id = request.user.id
        outbound_email = request.user.profile.outbound_email
        user_email = outbound_email if outbound_email else request.user.email
        user_name = request.user.profile.first_name
        last_name = request.user.profile.last_name
        template_id = temp_id
        opp_id = project_id
        contact_id = contact_id
        account_id = company_id
        subject = subject
        body = body
        email_template = EmailTemplate.objects.get(pk=template_id)
        template_type = email_template.type

        if template_type == EmailTemplate.PROJECT_BOARD:
            contact = ContactRole.objects.filter(opportunityid_id=project_id).values('name', 'email') \
                if contact_id is None else ContactRole.objects.filter(id=contact_id).values('name', 'email')
            contact_email = contact[0]['email']
            can_send_email = ProjectBoardEmailRule(request.user, opp_id, account_id, contact_id, template_id)
        else:
            contact = Contact.objects.filter(id=contact_id).values('name', 'email')
            contact_name = contact[0]['name']
            contact_email = contact[0]['email']
            can_send_email = GeneralContractorEmailRule(request.user, account_id, contact_id, template_id)
            body = body.replace('{CONTACT.NAME}', contact_name)
        if can_send_email.is_valid():
            email = EmailMessage(
                subject,
                body,
                from_email=f'{user_name} {last_name} <{user_email}>',
                to=[contact_email],
                reply_to=[contact_email],
            )
            email.content_subtype = 'html'

            if email.send():
                if template_type == UserEmail.PROJECT_BOARD:
                    UserEmail.objects.create(contact_id=contact_id, opportunity_id=opp_id,
                                             user_id=user_id, template_id=template_id, account_id=account_id,
                                             email_type=template_type, subject=subject, body=body)
                elif template_type == UserEmail.GENERAL_CONTRACTOR:

                    UserEmail.objects.create(company_contact_id=contact_id,
                                             user_id=user_id, template_id=template_id, account_id=account_id,
                                             email_type=template_type, subject=subject, body=body)

                return {"message": "email sent successfully"}
            return {'error': True, 'message': 'Email not sent'}


        else:
            message = can_send_email.get_error_message()
            return {'error': True, 'message': message}

    def send_mass_email(self, request, temp_id, company_id, contact_id, project_id, subject, body):
        user_id = request.user.id
        outbound_email = request.user.profile.outbound_email
        user_email = outbound_email if outbound_email else request.user.email
        user_name = request.user.profile.first_name
        last_name = request.user.profile.last_name
        template_id = temp_id
        opp_id = project_id
        contact_id = contact_id
        account_id = company_id
        subject = subject
        body = body
        email_template = EmailTemplate.objects.get(pk=template_id)
        template_type = email_template.type

        if template_type == EmailTemplate.PROJECT_BOARD:
            contact = ContactRole.objects.filter(opportunityid_id=project_id).values('name', 'email') \
                if contact_id is None else ContactRole.objects.filter(id=contact_id).values('name', 'email')
            contact_email = contact[0]['email']
            can_send_email = ProjectBoardEmailRule(request.user, opp_id, account_id, contact_id, template_id)
        else:
            contact = Contact.objects.filter(id=contact_id).values('name', 'email')
            contact_name = contact[0]['name']
            contact_email = contact[0]['email']
            can_send_email = GeneralContractorEmailRule(request.user, account_id, contact_id, template_id)
            body = body.replace('{CONTACT.NAME}', contact_name)
        if can_send_email.is_valid():
            email = EmailMessage(
                subject,
                body,
                from_email=f'{user_name} {last_name} <"brandon@constructioncleanpartners.com">',
                to=['mioshine2011@gmail.com'],
                reply_to=[contact_email],
            )
            email.content_subtype = 'html'

            if email.send():
                if template_type == UserEmail.PROJECT_BOARD:
                    UserEmail.objects.create(contact_id=contact_id, opportunity_id=opp_id,
                                             user_id=user_id, template_id=template_id, account_id=account_id,
                                             email_type=template_type, subject=subject, body=body)
                elif template_type == UserEmail.GENERAL_CONTRACTOR:

                    UserEmail.objects.create(company_contact_id=contact_id,
                                             user_id=user_id, template_id=template_id, account_id=account_id,
                                             email_type=template_type, subject=subject, body=body)

                return {"message": "email sent successfully"}
            return {'error': True, 'message': 'Email not sent'}


        else:
            message = can_send_email.get_error_message()
            return {'error': True, 'message': message}

    def process_send_mass_email(self):
        pass


class CheckAvailabilityEmail(generics.CreateAPIView):
    """
       List all snippets, or create a new snippet.
       """
    serializer_class = SendEmailSerializer
    queryset = UserEmail.objects.all()
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        try:
            if 'temp_id' not in request.data:
                return Response({"error": '*temp_id query params is required'}, status.HTTP_400_BAD_REQUEST)
            elif 'company_id' not in request.data:
                return Response({"error": '*company_id query params is required'}, status.HTTP_400_BAD_REQUEST)
            elif 'subject' not in request.data:
                return Response({"error": '*subject query params is required'}, status.HTTP_400_BAD_REQUEST)
            elif 'body' not in request.data:
                return Response({"error": '*body query params is required'}, status.HTTP_400_BAD_REQUEST)
            get_object_or_404(Opportunity, id=kwargs['project_id'])
            get_object_or_404(EmailTemplate, id=request.data['temp_id'])
            get_object_or_404(CompanyAccount, id=request.data['company_id'])

            temp_id = request.data['temp_id']
            company_id = request.data['company_id']
            subject = request.data['subject']
            body = request.data['body']
            if serializer.is_valid(raise_exception=True):
                result = self.send_email(request, temp_id, company_id, kwargs['project_id'], subject, body)
                if result.get('error') is not None:
                    return Response(result, status.HTTP_403_FORBIDDEN)

                return Response(result, status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Bad request {e}"}, status.HTTP_400_BAD_REQUEST)

    def send_email(self, request, temp_id, company_id, project_id, subject, body):
        user_id = request.user.id
        user_email = request.user.email
        user_name = request.user.account.fname
        last_name = request.user.account.lname
        template_id = temp_id
        opp_id = project_id
        account_id = company_id
        subject = subject
        body = body
        user = request.user
        email_template = EmailTemplate.objects.get(pk=template_id)
        template_type = email_template.type

        time_in_24hr = timezone.now() - timedelta(days=1)
        emails_region_count = UserEmail.objects.filter(user_id=user_id, opportunity_id=opp_id,
                                                       email_type=UserEmail.PROJECT_BOARD, account_id=account_id,
                                                       time_sent__gte=time_in_24hr).count()
        if emails_region_count < 1:
            contact = Contact.objects.get_contact_roles_by_project(company_id, user)
            if contact is not None:
                account_id = contact.account_id
                contact_list = contact.name.split(' ')
                first_name = contact_list[0] if len(contact_list) > 0 else contact_list
                temp_body, body = body.replace('{CONTACT.NAME}', first_name), body
                # celery_send_email.delay(user_name, last_name, contact.email, user_email, subject, body)

                if template_type == UserEmail.PROJECT_BOARD:
                    UserEmail.objects.create(
                        user_id=user_id, template_id=template_id,
                        account_id=account_id,
                        email_type=template_type,
                        opportunity_id=opp_id,
                    )
                elif template_type == UserEmail.GENERAL_CONTRACTOR:

                    UserEmail.objects.create(company_contact_id=contact.id,
                                             user_id=user_id, template_id=template_id,
                                             account_id=account_id,
                                             email_type=template_type,
                                             is_mass_email=True
                                             )

                return {'message': "email too sent successfully"}
        else:
            return {'message': f"You can only email contacts in this region"
                               " 1 times in 24 hours. Please come back tomorrow."}


@api_view(['POST'])
def send_verification_email(request):
    send_mail("New Domain Verification Request!", "Hey buddy, I want to verify my domain",
              request.user.email, ["support@ganarpro.com"])
    return Response({"message": f"Email sent"}, status.HTTP_200_OK)
