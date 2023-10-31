from django.utils.text import slugify
from djstripe.models import Subscription
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from app.api.gc_planify.models import GeneralContractor
from app.api.gc_planify.tasks import get_screenshot
from app.api.users.serializers import SubscriptionSerializer
import uuid


class GeneralContractorsSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email')
    user_type = serializers.SerializerMethodField(source='user.user_type')
    company_name = serializers.CharField(max_length=100, required=False, read_only=True)
    subscriptions = SerializerMethodField()

    def get_user_type(self, obj):
        return obj.user.get_user_type_display()

    def get_subscriptions(self, obj):
        subscriptions = SubscriptionSerializer(Subscription.objects.filter(customer_id=obj.customer),
                                               many=True).data
        return subscriptions

    class Meta:
        model = GeneralContractor
        fields = "__all__"

    def update(self, instance, validated_data):
        fields = {
            'first_name', 'last_name', 'phone', 'linkedin', 'plan_room_url','is_diversity_inclusion',
            'is_diversity_initiative',
            'pre_qualification_url', 'website', 'working_region', 'facebook','is_workforce_inclusion',
            'num_of_employees',
            'twitter', 'instagram', 'youtube', 'is_public', 'is_davis_bacon', 'is_diversity_champion',
            'is_annual_event',
            'is_add_itbs', 'is_talent_request', 'is_union', 'contact_name', 'contact_phone', 'contact_email',
            'is_diversity_certification', 'is_headhunter', 'is_increase_supplier_network', 'is_share_more', 'job_title'
        }
        for field in fields:
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))
        print(instance.__dict__)

        company_name = validated_data.get('company_name')
        if company_name:
            instance.company_name = company_name
            instance.company_slug = slugify(f"{company_name} {instance.company_slug.split('-')[-1]}")

        instance.save()
        return instance
