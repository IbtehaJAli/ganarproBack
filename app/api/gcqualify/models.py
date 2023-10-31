from django.db import models
from hashid_field import HashidAutoField
from app.api.authentication.models.user_registration import UserProfile
from app.api.models import TimestampedModel
from app.api.projects.models import CompanyAccount


class UserRegions(TimestampedModel):
    name = models.CharField(max_length=40, db_index=True)
    slug = models.CharField(max_length=20, db_index=True)

    def __str__(self):
        return self.id


class EmailSubscriber(TimestampedModel):
    id = HashidAutoField(prefix='gc_email', primary_key=True)
    email = models.EmailField(max_length=100, blank=False, null=False)


class PlanRoom(TimestampedModel):
    company_account = models.ForeignKey(CompanyAccount, null=True, related_name='plan_rooms',
                                        on_delete=models.SET_NULL)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name='plan_rooms')
    # region = models.ForeignKey(UserRegions, null=True, related_name='plan_rooms',
    #                            on_delete=models.SET_NULL)
    date_visited = models.DateField(null=True)
    note = models.TextField(null=True)


class PreQualify(TimestampedModel):
    company_account = models.ForeignKey(CompanyAccount, null=True, related_name='pre_qualify', on_delete=models.SET_NULL)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name='pre_qualify')
    upload = models.URLField(null=True)
    note = models.TextField(null=True)
