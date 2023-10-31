from abc import ABC
from datetime import datetime, timedelta

from django.utils import timezone

from app.api.emails.models import UserEmail


class EmailRuleType(ABC):

    def __init__(self, user, account, contact, template):
        self.no_of_organization_email_config = 0
        self.no_email_per_account_config = 0
        self.no_email_per_contact_config = 0
        self.no_of_template_per_contact_config = 0
        self.user = user
        self.account = account
        self.contact = contact
        self.template = template
        self.time_in_24hr = timezone.now() - timedelta(days=1)
        self.time_in_72hr = timezone.now() - timedelta(days=3)
        self.valid = True
        self.error_message = ""

    def can_send_organization_email(self):
        no_of_emails = UserEmail.objects.filter(
            user=self.user
            , time_sent__gte=self.time_in_24hr).count() + 1
        if no_of_emails > self.no_of_organization_email_config:
            self.valid = False
            self.set_error_message("You have sent 100 emails today, please wait until"
                                   " tomorrow to send another email.")
        return self.valid

    def can_send_email_to_contact(self):
        no_of_emails_per_contact = UserEmail.objects.filter(
            user=self.user, contact_id=self.contact
            , time_sent__gte=self.time_in_24hr).count() + 1
        if self.no_email_per_contact_config:
            if no_of_emails_per_contact > self.no_email_per_contact_config:
                self.valid = False
                self.set_error_message("You can not email the same contact twice in 1 day, choose another contact to "
                                       "email now or wait until tomorrow to send email to this contact.")
        return self.valid

    def can_use_template_per_contact(self):
        no_of_template_per_contact = UserEmail.objects.filter(
            user=self.user, contact_id=self.contact, template_id=self.template,
            time_sent__gte=self.time_in_24hr).count() + 1
        if self.no_of_template_per_contact_config:
            if no_of_template_per_contact > self.no_of_template_per_contact_config:
                self.valid = False
                self.set_error_message(" You can not use the same template 2 times on this contact in a 24 hour period."
                                       " Come back tomorrow to select this template again for this project, "
                                       "or select another template to email today")
        return self.valid

    def can_send_email_to_account(self):
        no_of_emails_per_account = UserEmail.objects.filter(
            user=self.user, account_id=self.account
            , time_sent__gte=self.time_in_24hr).count() + 1
        if self.no_email_per_account_config:
            if no_of_emails_per_account > self.no_email_per_account_config:
                self.valid = False
                self.set_error_message("You have sent 6 emails to this company within the last 24 hours."
                                       " Come back tomorrow to send the next email to this company.")
        return self.valid

    def set_error_message(self, error_message):
        self.error_message = error_message

    def get_error_message(self):
        return self.error_message


