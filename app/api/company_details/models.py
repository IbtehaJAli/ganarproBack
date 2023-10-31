from django.db import models
from app.api.authentication.models.user_registration import UserProfile


# Create your models here.
class BasicCompany(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='basic_company')
    company_name = models.CharField(max_length=100, null=True)
    office_address = models.CharField(max_length=200, null=True)
    office_city = models.CharField(max_length=200, null=True)
    office_state = models.CharField(max_length=200, null=True)
    office_zip = models.CharField(max_length=200, null=True)
    company_phone = models.CharField(max_length=20, null=True)
    company_fax = models.CharField(max_length=20, null=True)
    company_website = models.URLField(max_length=200, null=True)
    working_area = models.CharField(max_length=1000, null=True)
    company_specialty = models.CharField(max_length=200, null=True)
    company_person = models.CharField(max_length=100, null=True)
    company_email = models.EmailField(max_length=100, null=True)
    filled_fields = models.IntegerField(default=0)

    def __str__(self):
        return self.user.user.username


class CompanyInfo(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='company_info')
    company_address1 = models.TextField(max_length=100, null=True)
    company_city1 = models.TextField(max_length=50, null=True)
    company_state1 = models.TextField(max_length=50, null=True)
    company_zip1 = models.TextField(max_length=50, null=True)
    company_address2 = models.TextField(max_length=100, null=True)
    company_city2 = models.TextField(max_length=50, null=True)
    company_state2 = models.TextField(max_length=50, null=True)
    company_zip2 = models.TextField(max_length=50, null=True)
    company_employes_number = models.PositiveIntegerField(blank=True, null=True, default=0)
    permanent_employes = models.CharField(max_length=100, null=True)
    business_certified = models.CharField(max_length=10, null=True)  # Changed from BooleanField to CharField
    diversity_markets = models.CharField(max_length=1000, null=True)
    firm_name = models.CharField(max_length=100, null=True)
    dbe_certification = models.CharField(max_length=100, null=True)  # Changed from BooleanField to CharField
    mbe_certification = models.CharField(max_length=100, null=True)  # Changed from BooleanField to CharField
    wbe_certification = models.CharField(max_length=100, null=True)  # Changed from BooleanField to CharField
    interested_projects = models.TextField(max_length=1000, null=True)
    business_size = models.CharField(max_length=100, null=True)
    certificate_insurance = models.URLField(null=True)
    other_contacts = models.TextField(null=True)
    labor_affiliations = models.CharField(max_length=200, null=True)
    company_contract_type = models.CharField(max_length=100, null=True)
    union_market = models.CharField(max_length=500, null=True)  # Changed from BooleanField to CharField
    complaint_with_requirements = models.CharField(max_length=100, null=True)  # Changed from BooleanField to CharField
    complaint_with_state = models.CharField(max_length=100, null=True)  # Changed from BooleanField to CharField
    Inhouse = models.CharField(max_length=10, null=True)  # Changed from BooleanField to CharField
    apprentice_program = models.CharField(max_length=1000, null=True)  # Changed from BooleanField to CharField
    w9 = models.URLField(null=True)
    filled_fields = models.IntegerField(default=0)

    def __str__(self):
        return self.user.user.username


class Socials(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='socials')
    facebook_page = models.URLField(null=True)
    linkedin_page = models.URLField(null=True)
    instagram_page = models.URLField(null=True)
    twitter_page = models.URLField(null=True)
    filled_fields = models.IntegerField(default=0)

    def __str__(self):
        return self.user.user.username


class OrgDetails(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='org_details')
    identification_number = models.TextField(null=True, blank=True)
    date_started = models.TextField(null=True, blank=True)
    business_years = models.IntegerField(null=True, blank=True, default=0)
    parent_company = models.TextField(null=True, blank=True)
    state_founded = models.TextField(null=True, blank=True)
    organization_name = models.TextField(null=True, blank=True)
    years_under_name = models.IntegerField(null=True, blank=True, default=0)
    subsidiaries_number = models.IntegerField(null=True, blank=True, default=0)
    manager_name = models.TextField(null=True, blank=True)
    manager_email = models.EmailField(null=True, blank=True)
    entity_formation = models.TextField(null=True, blank=True)
    legal_entity = models.TextField(null=True, blank=True)
    legal_date = models.TextField(null=True, blank=True)
    registered_state = models.TextField(null=True, blank=True)
    license_type = models.TextField(null=True, blank=True)
    employee_orientation = models.TextField(null=True, blank=True)
    filled_fields = models.IntegerField(default=0)

    def __str__(self):
        return f"Org Details for {self.user.user.username}"


class ProjectHistory(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='project_history')
    project_size = models.TextField(null=True, blank=True)
    backlog = models.TextField(null=True, blank=True)
    failed_to_complete = models.TextField(null=True, blank=True)
    largest_contract_project = models.TextField(null=True, blank=True)
    largest_contract_amount = models.TextField(null=True, blank=True)
    largest_contract_completion_date = models.TextField(null=True, blank=True)
    jobs_awarded = models.IntegerField(null=True, blank=True)
    work_under_contract = models.IntegerField(null=True, blank=True)
    work_under_forces = models.TextField(null=True, blank=True)
    project_damages = models.TextField(null=True, blank=True)
    largest_contract_general = models.TextField(null=True, blank=True)
    largest_contract_contact = models.TextField(null=True, blank=True)
    filled_fields = models.IntegerField(default=0)

    def __str__(self):
        return f"Project History for {self.user.user.username}"


class CurrentWork(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='current_work')
    project1_info = models.TextField(null=True, blank=True)
    project1_contact = models.TextField(null=True, blank=True)
    project1_completion = models.TextField(null=True, blank=True)
    project1_self_work = models.TextField(null=True, blank=True)
    project2_info = models.TextField(null=True, blank=True)
    project2_contact = models.TextField(null=True, blank=True)
    project2_completion = models.TextField(null=True, blank=True)
    project2_self_work = models.TextField(null=True, blank=True)
    project3_info = models.TextField(null=True, blank=True)
    project3_contact = models.TextField(null=True, blank=True)
    project3_completion = models.TextField(null=True, blank=True)
    project3_self_work = models.TextField(null=True, blank=True)
    project4_info = models.TextField(null=True, blank=True)
    project4_contact = models.TextField(null=True, blank=True)
    project4_completion = models.TextField(null=True, blank=True)
    project4_self_work = models.TextField(null=True, blank=True)
    project5_info = models.TextField(null=True, blank=True)
    project5_contact = models.TextField(null=True, blank=True)
    project5_completion = models.TextField(null=True, blank=True)
    project5_self_work = models.TextField(null=True, blank=True)
    wip1_gc = models.TextField(null=True, blank=True)
    wip1_amount = models.TextField(null=True, blank=True)
    wip1_date_completion = models.TextField(null=True, blank=True)
    wip2_gc = models.TextField(null=True, blank=True)
    wip2_amount = models.TextField(null=True, blank=True)
    wip2_date_completion = models.TextField(null=True, blank=True)
    wip3_gc = models.TextField(null=True, blank=True)
    wip3_amount = models.TextField(null=True, blank=True)
    wip3_date_completion = models.TextField(null=True, blank=True)
    wip4_gc = models.TextField(null=True, blank=True)
    wip4_amount = models.TextField(null=True, blank=True)
    wip4_date_completion = models.TextField(null=True, blank=True)
    wip5_gc = models.TextField(null=True, blank=True)
    wip5_amount = models.TextField(null=True, blank=True)
    wip5_date_completion = models.TextField(null=True, blank=True)
    filled_fields = models.IntegerField(default=0)

    def __str__(self):
        return f"Current Work for {self.user.user.username}"


class CompletedWork(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='completed_work')
    project1_info = models.TextField(null=True, blank=True)
    project1_contact = models.TextField(null=True, blank=True)
    project1_percent_completed = models.TextField(null=True, blank=True)
    project2_info = models.TextField(null=True, blank=True)
    project2_contact = models.TextField(null=True, blank=True)
    project2_percent_completed = models.TextField(null=True, blank=True)
    project3_info = models.TextField(null=True, blank=True)
    project3_contact = models.TextField(null=True, blank=True)
    project3_percent_completed = models.TextField(null=True, blank=True)
    project4_info = models.TextField(null=True, blank=True)
    project4_contact = models.TextField(null=True, blank=True)
    project4_percent_completed = models.TextField(null=True, blank=True)
    project5_info = models.TextField(null=True, blank=True)
    project5_contact = models.TextField(null=True, blank=True)
    project5_percent_completed = models.TextField(null=True, blank=True)
    gc1_info = models.TextField(null=True, blank=True)
    gc1_amount = models.TextField(null=True, blank=True)
    gc1_date_completion = models.TextField(null=True, blank=True)
    gc2_info = models.TextField(null=True, blank=True)
    gc2_amount = models.TextField(null=True, blank=True)
    gc2_date_completion = models.TextField(null=True, blank=True)
    gc3_info = models.TextField(null=True, blank=True)
    gc3_amount = models.TextField(null=True, blank=True)
    gc3_date_completion = models.TextField(null=True, blank=True)
    gc4_info = models.TextField(null=True, blank=True)
    gc4_amount = models.TextField(null=True, blank=True)
    gc4_date_completion = models.TextField(null=True, blank=True)
    gc5_info = models.TextField(null=True, blank=True)
    gc5_amount = models.TextField(null=True, blank=True)
    gc5_date_completion = models.TextField(null=True, blank=True)
    filled_fields = models.IntegerField(default=0)

    def __str__(self):
        return f"Completed Work for {self.user.user.username}"


class Insurance(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='insurance')
    agent_name = models.TextField(null=True, blank=True)
    agent_contact = models.TextField(null=True, blank=True)
    agent_phone = models.TextField(null=True, blank=True)
    agent_email = models.TextField(null=True, blank=True)
    agent_website = models.URLField(null=True, blank=True)
    insurance_expiry = models.TextField(null=True, blank=True)
    emr_carrier = models.TextField(null=True, blank=True)
    emr_letter = models.URLField(null=True, blank=True)
    bonding_company_letter = models.URLField(null=True, blank=True)
    liability_coverage = models.TextField(null=True, blank=True)
    general_aggregate = models.TextField(null=True, blank=True)
    excess_limit = models.TextField(null=True, blank=True)
    auto_insurance_limit = models.TextField(null=True, blank=True)
    compensation_limit = models.TextField(null=True, blank=True)
    modification_rate = models.TextField(null=True, blank=True)
    bond_capacity = models.TextField(null=True, blank=True)
    surety_bonding_company = models.TextField(null=True, blank=True)
    cgl_policy = models.TextField(null=True, blank=True)
    current_work_bonded = models.TextField(null=True, blank=True)
    surety_rating = models.TextField(null=True, blank=True)
    performance_bond = models.TextField(null=True, blank=True)
    filled_fields = models.IntegerField(default=0)

    def __str__(self):
        return f"Insurance for {self.user.user.username}"


class Safety(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='safety')
    incident_rate_2023 = models.TextField(null=True, blank=True)
    incident_rate_2022 = models.TextField(null=True, blank=True)
    incident_rate_2021 = models.TextField(null=True, blank=True)
    incident_rate_2020 = models.TextField(null=True, blank=True)
    osha_citations = models.IntegerField(null=True, blank=True, default=0)
    fatalities = models.IntegerField(null=True, blank=True, default=0)
    written_safety_health = models.TextField(null=True, blank=True)
    safety_program = models.TextField(null=True, blank=True)
    job_safety = models.TextField(null=True, blank=True)
    hazard_communication_program = models.TextField(null=True, blank=True)
    accident_investigation_program = models.TextField(null=True, blank=True)
    field_safety_inspectors = models.TextField(null=True, blank=True)
    osha_logs = models.URLField(null=True)
    safety_manual = models.URLField(null=True)
    safety_contact = models.TextField(null=True, blank=True)
    warranty_contact = models.TextField(null=True, blank=True)
    incidents_in_2023 = models.TextField(null=True, blank=True)
    incidents_in_2022 = models.TextField(null=True, blank=True)
    incidents_in_2021 = models.TextField(null=True, blank=True)
    incidents_in_2020 = models.TextField(null=True, blank=True)
    most_hours_worked_employee = models.TextField(null=True, blank=True)
    employee_hours_in_2023 = models.TextField(null=True, blank=True)
    employee_hours_in_2022 = models.TextField(null=True, blank=True)
    employee_hours_in_2021 = models.TextField(null=True, blank=True)
    employee_hours_in_2020 = models.TextField(null=True, blank=True)
    project_safety_plans = models.TextField(null=True, blank=True)
    abuse_policy = models.TextField(null=True, blank=True)
    return_to_work_program = models.TextField(null=True, blank=True)
    filled_fields = models.IntegerField(default=0)

    def __str__(self):
        return f"Safety for {self.user.user.username}"


class Finance(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='finance')
    duns_number = models.TextField(null=True, blank=True)
    dun_bradstreet_rating = models.TextField(null=True, blank=True)
    credit_used_against = models.TextField(null=True, blank=True)
    line_credit = models.TextField(null=True, blank=True)
    current_year_revenue = models.TextField(null=True, blank=True)
    interested_in_job_size = models.TextField(null=True, blank=True)
    date_financials = models.TextField(null=True, blank=True)
    primary_bank_name = models.TextField(null=True, blank=True)
    bank_reference_name = models.TextField(null=True, blank=True)
    banker_phone = models.TextField(null=True, blank=True)
    naics = models.TextField(null=True, blank=True)
    equipments_owned_value = models.TextField(null=True, blank=True)
    bond_rate = models.TextField(null=True, blank=True)
    accountant_firm_name = models.TextField(null=True, blank=True)
    accountant_phone = models.TextField(null=True, blank=True)
    financials_last_year = models.URLField(null=True, blank=True)
    current_year_volume = models.TextField(null=True, blank=True)
    largest_contract_2023 = models.TextField(null=True, blank=True)
    largest_contract_2022 = models.TextField(null=True, blank=True)
    largest_contract_2021 = models.TextField(null=True, blank=True)
    largest_contract_2020 = models.TextField(null=True, blank=True)
    largest_contract_2019 = models.TextField(null=True, blank=True)
    revenue_2023 = models.TextField(null=True, blank=True)
    revenue_2022 = models.TextField(null=True, blank=True)
    revenue_2021 = models.TextField(null=True, blank=True)
    revenue_2020 = models.TextField(null=True, blank=True)
    revenue_2019 = models.TextField(null=True, blank=True)
    company1 = models.TextField(null=True, blank=True)
    creditor1_contact = models.TextField(null=True, blank=True)
    creditor1_phone = models.TextField(null=True, blank=True)
    creditor1_balance = models.TextField(null=True, blank=True)
    company2 = models.TextField(null=True, blank=True)
    creditor2_contact = models.TextField(null=True, blank=True)
    creditor2_phone = models.TextField(null=True, blank=True)
    creditor2_balance = models.TextField(null=True, blank=True)
    filled_fields = models.IntegerField(default=0)

    def __str__(self):
        return f"Finance for {self.user.user.username}"


class Supplier(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='supplier')
    supplier1_name = models.TextField(null=True, blank=True)
    supplier1_website = models.TextField(null=True, blank=True)
    supplier2_name = models.TextField(null=True, blank=True)
    supplier2_website = models.TextField(null=True, blank=True)
    supplier3_name = models.TextField(null=True, blank=True)
    supplier3_website = models.TextField(null=True, blank=True)
    supplier1_phone = models.TextField(null=True, blank=True)
    supplier1_industry = models.TextField(null=True, blank=True)
    supplier2_phone = models.TextField(null=True, blank=True)
    supplier2_industry = models.TextField(null=True, blank=True)
    supplier3_phone = models.TextField(null=True, blank=True)
    supplier3_industry = models.TextField(null=True, blank=True)
    filled_fields = models.IntegerField(default=0)

    def __str__(self):
        return f"Supplier for {self.user.user.username}"


class Legal(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='legal')
    involved_in_litigation = models.TextField(null=True, blank=True)
    involved_in_bankruptcy = models.TextField(null=True, blank=True)
    criminal_investigation = models.TextField(null=True, blank=True)
    filled_fields = models.IntegerField(default=0)

    def __str__(self):
        return f"Legal for {self.user.user.username}"


class ShippingReceivings(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='shipping_receivings')
    fedex = models.TextField(null=True, blank=True)
    ups = models.TextField(null=True, blank=True)
    filled_fields = models.IntegerField(default=0)

    def __str__(self):
        return f"Shipping/Receivings for {self.user.user.username}"