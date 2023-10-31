from datetime import datetime, timedelta

from app.api.emails.models import EmailRule
from app.api.emails.service.email_rule_setup.EmailRuleType import EmailRuleType


class GeneralContractorEmailRule(EmailRuleType):

    def __init__(self, user, account, contact, template):

        super().__init__(user, account, contact, template)

        self.rules_setup = EmailRule.objects.filter(type=EmailRule.GENERAL_CONTRACTOR).order_by('-modified').first()
        self.no_of_organization_email_config = self.rules_setup.organization_wide_email or 0
        self.no_email_per_contact_config = self.rules_setup.email_per_contact or 0
        self.no_email_per_account_config = self.rules_setup.email_per_account or 0
        self.no_of_template_per_contact_config = self.rules_setup.template_per_contact or 0

    def is_valid(self):
        if not self.can_use_template_per_contact():
            return self.valid
        elif not self.can_send_email_to_contact():
            return self.valid
        elif not self.can_send_email_to_account():
            return self.valid
        elif not self.can_send_organization_email():
            return self.valid
        return self.valid


