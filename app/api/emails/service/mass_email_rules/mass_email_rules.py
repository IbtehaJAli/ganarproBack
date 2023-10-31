# services.py
from django.utils import timezone
from datetime import datetime, timedelta
from app.api.emails.models import UserEmail


class MassEmailServiceRule:

    def __init__(self, user, opportunity, contact, account):
        self.user = user
        self.account = account
        self.opportunity = opportunity
        self.contact = contact
        self.time_in_24hr = timezone.now() - timedelta(days=1)

    def has_daily_limit_exceeded(self):
        return UserEmail.objects.filter(user=self.user, opportunity=self.opportunity,
                                        contact=self.contact, account=self.account,
                                        time_sent__gte=self.time_in_24hr).exists()

    def has_mass_total_limit_exceeded(self):
        return UserEmail.objects.filter(user=self.user, opportunity=self.opportunity).count() > 50

    def has_total_limit_exceeded(self):
        return UserEmail.objects.filter(user=self.user, opportunity=self.opportunity).count() >= 3

    def has_contact_received_email(self):
        return UserEmail.objects.filter(user=self.user, contact=self.contact, template_type='ME').exists()


