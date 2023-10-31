from django.db import models
from app.api.authentication.models.user_registration import User
# Create your models here.

# Create your models here.
from app.api.models import TimestampedModel
from app.api.project_type.models import ProjectType


class PricingModel(TimestampedModel):
    project_type = models.CharField(max_length=50, blank=True, null=False)
    rough = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=False)
    final = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=False)
    fluff = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=False)
    rough_final = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=False)
    rough_fluff = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=False)
    final_fluff = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=False)
    rough_final_fluff = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=False)

    def __str__(self):
        return self.project_type


class StateLaborPrice(TimestampedModel):
    area_name = models.CharField(max_length=50, blank=True, null=False)
    average_labor_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    percentage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_customer = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    one_day_work = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.area_name


class CleanUPEstimates(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False,
                             related_name='user_cleanup_estimates')
    square_foot = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=False)
    living_unit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    emergency_pricing = models.BooleanField(default=False, blank=True, null=True)
    project_name = models.CharField(max_length=100, blank=False, null=False)
    project_type = models.CharField(max_length=100, blank=True, null=False)
    phase = models.CharField(max_length=100, blank=True, null=True)
    not_sure = models.CharField(max_length=10, blank=True, null=True)
    no_stories = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_per1_bed = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_per2_bed = models.IntegerField(blank=True, null=True)
    price_per3_bed = models.IntegerField(blank=True, null=True)
    no_stories_check = models.BooleanField(default=False, blank=True, null=True)
    no_of_unit1_bed = models.CharField(max_length=10, blank=True, null=True)
    no_of_unit2_bed = models.CharField(max_length=10, blank=True, null=True)
    no_of_unit3_bed = models.CharField(max_length=10, blank=True, null=True)
    use_unit_pricing = models.BooleanField(default=False, blank=True, null=True)
    scrubbing_pricing = models.BooleanField(default=False, blank=True, null=True)
    use_living_unit_pricing = models.BooleanField(default=False, blank=True, null=True)
    laborersOnSite = models.IntegerField(blank=True, null=True)
    hours_crew_works_daily = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    hourly_labor_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    noOfDaysExpected = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    job_over_head = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    profit_margin = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    job_costs_over_head = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    use_price_per_day = models.BooleanField(default=False, blank=True, null=True)
    use_number_of_days = models.BooleanField(default=False, blank=True, null=True)
    window_panes = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pressure_wash = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_per_window = models.DecimalField(max_digits=10, decimal_places=2, default=5, blank=True, null=True)
    pressure_wash_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.1,  blank=True, null=True)
    accurate_days_on_site = models.IntegerField(blank=True, null=True, default=0)
    use_accurate_days_on_site = models.BooleanField(default=False, blank=True, null=True)
