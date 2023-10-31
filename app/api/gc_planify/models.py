from django.db import models
from djstripe.models import Customer, Subscription

from app.api.authentication.models.user_registration import  User


# Create your models here.

class GeneralContractor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='general_contractor')
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name='general_contractors')
    subscription = models.ForeignKey(Subscription, null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name='general_contractors')
    first_name = models.CharField('First Name', max_length=100, blank=False, null=True)
    last_name = models.CharField('Last Name', max_length=100, blank=False, null=True)
    phone = models.CharField(blank=True, null=True, max_length=20)
    company_name = models.CharField(max_length=100, null=True, blank=False)
    company_slug = models.CharField(max_length=100, null=True, unique=True, blank=False, db_index=True)
    working_region = models.JSONField(max_length=100, null=True, blank=True)
    pre_qualification_url = models.URLField(max_length=1000, null=True, blank=True)
    pre_qualification_img_url = models.URLField(max_length=1000, null=True, blank=True)
    plan_room_url = models.URLField(max_length=1000, null=True, blank=True)
    plan_room_img_url = models.URLField(max_length=1000, null=True)
    website = models.URLField(max_length=1000, null=True,blank=True)
    website_img_url = models.URLField(max_length=500, null=True,blank=True)
    linkedin = models.URLField(max_length=1000, null=True, blank=True)
    linkedin_img_url = models.URLField(max_length=5000, null=True, blank=True)
    facebook = models.URLField(max_length=1000, null=True, blank=True)
    facebook_img_url = models.URLField(max_length=500, null=True,blank=True)
    twitter = models.URLField(max_length=1000, null=True,blank=True)
    twitter_img_url = models.URLField(max_length=500, null=True, blank=True)
    instagram = models.URLField(max_length=1000, null=True, blank=True)
    instagram_img_url = models.URLField(max_length=500, null=True, blank=True)
    youtube = models.URLField(max_length=1000, null=True,blank=True)
    youtube_img_url = models.URLField(max_length=500, null=True, blank=True)
    is_public = models.BooleanField(max_length=10, null=True, default=False, blank=True)
    is_davis_bacon = models.BooleanField(max_length=10, null=True, default=False, blank=True)
    is_add_itbs = models.BooleanField(max_length=10, null=True, default=False, blank=True)
    is_talent_request = models.BooleanField(max_length=10, null=True, default=False, blank=True)
    is_union = models.BooleanField(max_length=10, null=True, default=False,blank=True)
    # Diversity and Inclusion Section
    is_diversity_inclusion = models.BooleanField(default=False, blank=True, null=True)
    is_diversity_initiative = models.BooleanField(default=False, blank=True, null=True)
    is_workforce_inclusion = models.BooleanField(default=False, blank=True, null=True)
    num_of_employees = models.PositiveIntegerField(null=True, blank=True)
    is_diversity_champion = models.BooleanField(default=False, blank=True, null=True)
    contact_name = models.CharField(max_length=255, null=True, blank=True)
    contact_phone = models.CharField(max_length=255, null=True, blank=True)
    job_title = models.CharField(max_length=255, null=True, blank=True)
    contact_email = models.EmailField(max_length=255, null=True, blank=True)
    is_annual_event = models.BooleanField(default=False, blank=True, null=True)
    is_diversity_certification = models.BooleanField(default=False, blank=True, null=True)

    # Service Request Section
    is_headhunter = models.BooleanField(default=False, blank=True, null=True)
    is_increase_supplier_network = models.BooleanField(default=False, blank=True, null=True)
    is_share_more = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        db_table = "general_contractors"
