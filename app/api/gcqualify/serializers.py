from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers

from app.api.gcqualify.models import UserRegions, CompanyAccount, PlanRoom


class RegionsSerializer(serializers.ModelSerializer):
    # id = HashidSerializerCharField(source_field='gcqualify.UserRegions.id', read_only=True)

    class Meta:
        model = UserRegions
        fields = ('id', 'name', 'slug')


class PlanRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanRoom
        fields = ('id', 'company_account', 'user_profile', 'date_visited')
