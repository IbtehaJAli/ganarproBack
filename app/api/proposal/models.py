from django.db import models

from app.api.authentication.models.user_registration import User
# Create your models here.
from app.api.models import TimestampedModel
from app.api.project_type.models import ProjectType


class Proposal(TimestampedModel):
    """Proposal table"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False,
                             related_name='user_proposals')
    project_type = models.ForeignKey(ProjectType, on_delete=models.SET_NULL, null=True, blank=False,
                                              related_name='project_type_proposals')
    project_name = models.CharField(max_length=50, blank=False, null=False)
    project_street = models.CharField(max_length=150, blank=True, null=False)
    project_city = models.CharField(max_length=150, blank=True, null=True)
    project_state = models.CharField(max_length=150, blank=True, null=True)
    project_zip = models.CharField(max_length=150, blank=True, null=True)
    bid_amount = models.CharField(max_length=150, blank=True, null=True)
    project_contact_1_name = models.CharField(max_length=150, blank=True, null=True)
    project_contact_1_email = models.CharField(max_length=150, blank=True, null=True)
    project_contact_1_phone = models.CharField(max_length=150, blank=True, null=True)
    project_contact_2_name = models.CharField(max_length=150, blank=True, null=True)
    project_contact_2_email = models.CharField(max_length=150, blank=True, null=True)
    project_contact_2_phone = models.CharField(max_length=150, blank=True, null=True)
    customer_company_name = models.CharField(max_length=150, blank=True, null=True)
    customer_street = models.CharField(max_length=150, blank=True, null=True)
    customer_state = models.CharField(max_length=150, blank=True, null=True)
    customer_city = models.CharField(max_length=150, blank=True, null=True)
    customer_zip = models.CharField(max_length=150, blank=True, null=True)
    company_name = models.CharField(max_length=150, blank=False, null=False)
    company_street = models.CharField(max_length=150, blank=True, null=True)
    company_state = models.CharField(max_length=150, blank=True, null=True)
    company_city = models.CharField(max_length=150, blank=True, null=True)
    company_zip = models.CharField(max_length=150, blank=True, null=True)
    company_contact_name = models.CharField(max_length=150, blank=True, null=True)
    company_contact_email = models.CharField(max_length=150, blank=True, null=True)
    company_contact_phone = models.CharField(max_length=150, blank=True, null=True)
    proposal_point_contact_name = models.CharField(max_length=150, blank=True, null=True)
    proposal_point_contact_email = models.CharField(max_length=150, blank=True, null=True)
    proposal_point_contact_phone = models.CharField(max_length=150, blank=True, null=True)
    job_site_contact_name = models.CharField(max_length=150, blank=True, null=True)
    job_site_contact_email = models.CharField(max_length=150, blank=True, null=True)
    job_site_contact_phone = models.CharField(max_length=150, blank=True, null=True)
    company_state_short = models.CharField(max_length=150, blank=True, null=True)
    current_date = models.CharField(max_length=150, blank=True, null=True)
    ffile_url = models.URLField(null=True)

    def __str__(self):
        return self.project_name
