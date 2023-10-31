from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from app.api.projects.models import Opportunity, CompanyAccount, HotScope


class CompanyAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAccount
        fields = ('id', 'name', 'prequalification_application', 'billing_city', 'billing_state', 'planroom_link',
                  'opportunity_source_stage_type')


class ProjectSerializer(serializers.ModelSerializer):
    # company = SerializerMethodField()
    company_market_working_region = SerializerMethodField()
    sf_size_str = serializers.CharField(read_only=True)
    no_of_contacts = serializers.IntegerField(read_only=True)
    no_of_email_sent = serializers.IntegerField(read_only=True)
    last_email_sent = serializers.DateTimeField(read_only=True)

    def get_company_market_working_region(self, obj):
        try:
            market_region = CompanyAccount.objects.get(account_id=obj.company_account_id).market_working_region
        except CompanyAccount.DoesNotExist:
            market_region = None
        return market_region

    class Meta:
        model = Opportunity
        fields = ('id', 'oppid', 'name', 'address', 'city', 'state_short', 'state', 'zip_code', 'account_name',
                  'description', 'opportunity_package', 'plan_drawings', 'created_date', 'last_modified_date',
                  'when_c', 'bid_due_date', 'units', 'sf_size', 'sf_size_str', 'stage_name', 'project_type',
                  'send_partner_details', 'close_date', 'pipdcmkr_approval', 'account_billing_address', 'account_phone',
                  'account_website', 'last_modified_date_simple', 'hot_lead_trade_scope', 'url_slug', 'negative_scope',
                  'country', 'status', 'project_completion', 'davis_bacon_prevailing_wage_detail', 'laborer_union',
                  'primary_contact_name', 'site_contact_name', 'primary_contact_phone', 'created', 'modified',
                  'primary_contact_email', 'site_contact_email', 'site_contact_phone', 'latitude', 'longitude',
                  'est_break_ground_date', 'company_market_working_region', 'no_of_contacts', 'no_of_email_sent',
                  'last_email_sent'
                  )


class HotScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotScope
        fields = ('name', 'slug', 'amount')


class OpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunity
        fields = ['oppid', 'name', 'latitude', 'longitude', 'address', 'city', 'state']  # Add other fields as needed
