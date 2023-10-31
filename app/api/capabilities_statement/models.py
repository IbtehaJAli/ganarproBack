from django.db import models
from app.api.authentication.models.user_registration import UserProfile


# Create your models here.
class capability_statement(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='capability_statement')
    header_name = models.CharField(max_length=100, default="CAPABILITIES STATEMENT")
    logo_image = models.URLField(null=True, blank=True)
    pdf_name = models.CharField(max_length=50)
    version = models.CharField(max_length=200)
    company_info = models.CharField(max_length=100, null=True)
    company_address1 = models.CharField(max_length=150, null=True)
    company_address2 = models.CharField(max_length=150, null=True)
    owner_name = models.CharField(max_length=100, null=True)
    owner_phone = models.CharField(max_length=100, null=True)
    owner_email = models.CharField(max_length=100, null=True)
    url = models.URLField(null=True, blank=True)
    about_us = models.CharField(max_length=500, null=True)
    about_us_header = models.CharField(max_length=100, null=True)
    core_competencies = models.CharField(max_length=200, null=True)
    core_competencies_info = models.CharField(max_length=200, null=True)
    core_competencies_header = models.CharField(max_length=100, null=True)
    core_competencies_image = models.URLField(null=True, blank=True)
    past_performance = models.CharField(max_length=500, null=True)
    past_performance_image = models.URLField(null=True, blank=True)
    past_performance_header = models.CharField(max_length=100, null=True)
    difference = models.CharField(max_length=500, null=True)
    difference_bullets = models.CharField(max_length=500, null=True)
    difference_header = models.CharField(max_length=100, null=True)
