from django.db import models

from app.api.authentication.models import User
from app.api.email_templates.models import EmailTemplate

from app.api.emails.utils import send_email
from app.api.models import TimestampedModel
from app.api.projects.models import CompanyAccount, Opportunity, Contact, ContactRole


# Create your models here.

class UserEmailManager(models.Manager):
    def get_user_emails(self, user):
        return self.get_queryset().filter(user=user, email_type='PB').order_by('-time_sent').extra(
            select={'opp_name': 'SELECT name FROM "search_opportunity" '
                                'WHERE "search_useremail".opportunity_id = "search_opportunity".id',
                    'opp_url_slug': 'SELECT url_slug FROM "search_opportunity" '
                                    'WHERE "search_useremail".opportunity_id = "search_opportunity".id',
                    'template_name': 'SELECT name FROM "search_emailtemplate" '
                                     'WHERE "search_useremail".template_id = "search_emailtemplate".id',
                    'contact_name': 'SELECT  name FROM "search_contactrole" '
                                    'WHERE search_useremail.contact_id = search_contactrole.id',
                    'general_contractor': 'SELECT  name FROM "search_companyaccount" '
                                          'WHERE "search_useremail".account_id= "search_companyaccount".id',
                    })

    def get_user_emails_company(self, user):
        return self.get_queryset().filter(user=user, email_type='GC').order_by('-time_sent').extra(
            select={
                'template_name': 'SELECT name FROM "search_emailtemplate" '
                                 'WHERE "search_useremail".template_id = "search_emailtemplate".id',
                'contact_slug': 'SELECT search_contact.slug FROM "search_contact" '
                                'WHERE "search_useremail".company_contact_id = "search_contact".id',
                'contact_name': 'SELECT  name FROM "search_contact" '
                                'WHERE search_useremail.company_contact_id = search_contact.id',
                'company_slug': 'SELECT search_companyaccount.slug FROM "search_companyaccount" '
                                'WHERE "search_useremail".account_id = "search_companyaccount".id',
                'general_contractor': 'SELECT  name FROM "search_companyaccount" '
                                      'WHERE "search_useremail".account_id= "search_companyaccount".id',
            })

    def time_sent_and_email_count_per_project(self, user, oppid):
        qs = self.get_queryset()
        user_emails = qs.filter(user=user, opportunity_id=oppid, email_type='PB')
        user_emails_count = user_emails.count()
        try:
            user_emails_result = user_emails.latest('time_sent')
            time_sent = user_emails_result.time_sent
        except UserEmail.DoesNotExist:
            time_sent = ''
        return time_sent, user_emails_count

    def time_sent_and_email_count_per_company(self, user, account_id):
        qs = self.get_queryset()
        user_emails = qs.filter(user=user, account_id=account_id)
        user_emails_count = user_emails.count()
        try:
            user_emails_result = user_emails.latest('time_sent')
            time_sent = user_emails_result.time_sent
        except UserEmail.DoesNotExist:
            time_sent = ''
        return time_sent, user_emails_count

    def email_count(self, user):
        qs = self.get_queryset()
        user_emails = qs.filter(user=user)
        user_emails_count = user_emails.count()
        return user_emails_count


class UserEmail(models.Model):
    contact = models.ForeignKey(ContactRole, null=True, related_name='user_emails', db_index=True,
                                on_delete=models.SET_NULL)
    company_contact = models.ForeignKey(Contact, null=True, related_name='user_emails', db_index=True,
                                        on_delete=models.SET_NULL)
    opportunity = models.ForeignKey(Opportunity, null=True, related_name='user_emails', db_index=True,
                                    on_delete=models.CASCADE)
    account = models.ForeignKey(CompanyAccount, null=True, related_name='user_emails', db_index=True,
                                on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_emails', db_index=True, )
    time_sent = models.DateTimeField(auto_now_add=True)
    template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True, related_name='user_emails',
                                 db_index=True, )
    slug = models.SlugField(max_length=3000, null=True)
    GENERAL_CONTRACTOR = 'GC'
    PROJECT_BOARD = 'PB'
    MASS_EMAIL = 'ME'
    EMAIL_TYPE = (
        (GENERAL_CONTRACTOR, 'General Contractor'),
        (PROJECT_BOARD, 'Project Board'),
        (MASS_EMAIL, 'Mass Email')
    )
    email_type = models.CharField(max_length=2, null=True, choices=EMAIL_TYPE)
    region = models.CharField(max_length=20, null=True)
    subject = models.TextField(null=True, blank=False)
    body = models.TextField(null=True, blank=False)
    is_mass_email = models.BooleanField(null=True, default=False)

    objects = UserEmailManager()

    class Meta:
        ordering = ['-time_sent']
        get_latest_by = 'time_sent'

    def __str__(self):
        return f"{self.user.first_name} Email"


class EmailRule(TimestampedModel):
    """
    time assumed is 24hr
    """
    organization_wide_email = models.IntegerField(help_text='100 maximum emails organization wide per 24hr')
    email_per_project = models.IntegerField(help_text='At maximum 2 emails per project per 24hr')
    email_per_contact = models.IntegerField(help_text='At maximum 1 email to contact per 24hr')
    email_per_account = models.IntegerField(help_text='At maximum 6 emails per account per 24 hr period.')
    template_per_project = models.IntegerField(
        help_text='Email template can be used at maximum 1 time per project per 24hr.')
    # time assumed is 72hr
    template_per_contact = models.IntegerField(help_text='Can not send the same template back to back to a contact')

    GENERAL_CONTRACTOR = 'GC'
    PROJECT_BOARD = 'PB'
    EMAIL_RULE_TYPE = (
        (GENERAL_CONTRACTOR, 'General Contractor'),
        (PROJECT_BOARD, 'Project Board')
    )
    type = models.CharField(max_length=2, choices=EMAIL_RULE_TYPE, blank=False, null=True, default=PROJECT_BOARD)

    def __str__(self):
        return "Email Rule Setup"

    class Meta:
        ordering = ['-modified']


class EmailManager(models.Manager):

    def send_mass_email(self, user, opportunity_ids, subject, body, template_id, template_type):
        from app.api.emails.service.mass_email_rules.mass_email_rules import MassEmailServiceRule
        sent_emails_count = 0

        for opportunity_id in opportunity_ids:

            opportunity = Opportunity.objects.get(id=opportunity_id)
            company_account = CompanyAccount.objects.get(account_id=opportunity.company_account_id)

            sent_contact_ids = UserEmail.objects.filter(
                opportunity=opportunity, email_type='ME'
            ).values_list('contact_id', flat=True)
            contacts = opportunity.contact_roles.exclude(
                id__in=sent_contact_ids
            ).all()

            if contacts:
                contact = contacts[0]
            elif len(opportunity_ids) == 1 and not contacts:
                return {'error': True, 'message': 'You can only send one message per contact using mass email'}
            else:
                print('here 3')
                continue

            mass_email_rule = MassEmailServiceRule(user, opportunity, contact, company_account)

            # for contact in contacts:
            #     if sent_emails_count >= 50:
            #         return  # Max 50 emails per day
            if sent_emails_count == 50:
                break

            # Validate the rules before sending the email
            if (not mass_email_rule.has_daily_limit_exceeded() and
                    not mass_email_rule.has_total_limit_exceeded()):

                try:
                    send_email(user.profile, contact, subject, body)
                    sent_emails_count += 1

                    UserEmail.objects.create(contact=contact, opportunity=opportunity,
                                             user=user, template_id=template_id, account=company_account,
                                             email_type=template_type, subject=subject, body=body)
                except Exception as e:
                    print(f"User {user.outbound_email}  Sending email to {contact.email}")

        return {"message": "email sent successfully"}



