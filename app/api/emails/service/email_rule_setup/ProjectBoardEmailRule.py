from datetime import datetime, timedelta

from django.utils import timezone

from app.api.emails.models import EmailRule, UserEmail
from app.api.emails.service.email_rule_setup.EmailRuleType import EmailRuleType


class ProjectBoardEmailRule(EmailRuleType):

    def __init__(self, user, project, account, contact, template):
        super().__init__(user, account, contact, template)
        self.project = project

        self.rules_setup = EmailRule.objects.filter(type=EmailRule.PROJECT_BOARD).order_by('-modified').first()
        self.no_of_organization_email_config = self.rules_setup.organization_wide_email or 0
        self.no_email_per_project_config = self.rules_setup.email_per_project or 0
        self.no_email_per_contact_config = self.rules_setup.email_per_contact or 0
        self.no_email_per_account_config = self.rules_setup.email_per_account or 0
        self.no_template_per_project_config = self.rules_setup.template_per_project or 0
        self.no_of_template_per_contact_config = self.rules_setup.template_per_contact or 0

    def is_valid(self):
        if not self.can_use_template_per_project():
            return self.valid
        if not self.can_use_template_per_contact():
            return self.valid
        elif not self.can_send_email_to_contact():
            return self.valid
        elif not self.can_send_email_to_account():
            return self.valid
        elif not self.can_send_email_to_project():
            return self.valid
        elif not self.can_send_organization_email():
            return self.valid
        return self.valid

    def can_send_email_to_project(self):
        no_of_emails_per_project = UserEmail.objects.filter(
            user=self.user, opportunity_id=self.project
            , time_sent__gte=self.time_in_24hr).count() + 1
        if self.no_email_per_project_config:
            if no_of_emails_per_project > self.no_email_per_project_config:
                self.valid = False
                self.set_error_message("You can only email this project"
                                       " 2 times in 24 hours. Please come back tomorrow.")
        return self.valid

    def can_use_template_per_project(self):
        no_template_per_project = UserEmail.objects.filter(
            user=self.user, opportunity_id=self.project, template_id=self.template,
            time_sent__gte=self.time_in_24hr).count() + 1
        if self.no_template_per_project_config:
            if no_template_per_project > self.no_template_per_project_config:
                self.valid = False
                self.set_error_message(" You can not use the same template 2 times on this project in a 24 hour period."
                                       " Come back tomorrow to select this template again for this project, "
                                       "or select another template to email today")
        return self.valid



