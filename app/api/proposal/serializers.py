from rest_framework import serializers

from app.api.authentication.models import User
from app.api.project_type.serializers import ProjectTypeSerializer
from app.api.proposal.models import Proposal
from app.api.users.serializers import UserSerializer, UserProfileSerializer


class ProposalSerializer(serializers.ModelSerializer):

    # user_id = serializers.PrimaryKeyRelatedField(
    #     source='user',
    #     queryset=User.objects.all()
    # )
    project_type = ProjectTypeSerializer(read_only=True)

    class Meta:
        model = Proposal
        fields = '__all__'

    #
    # def get_field_names(self, declared_fields, info):
    #     expanded_fields = super(ProposalSerializer, self).get_field_names(declared_fields, info)
    #
    #     if getattr(self.Meta, 'extra_fields', None):
    #         return expanded_fields + self.Meta.extra_fields
    #     else:
    #         return expanded_fields


# class SubscriptionSerializer(serializers.ModelSerializer):
#     attom_id = serializers.IntegerField(allow_null=True, required=False)
#     property_address_full = serializers.CharField(
#         required=True,
#         allow_null=False,
#         error_messages={
#             "required": error_dict["required"].format("property_address_full"),
#             "blank": error_dict["blank"].format("property_address_full"),
#         },
#     )
#
#     hvac_cooling_detail_code = serializers.IntegerField(allow_null=True, required=False)
#     hvac_heating_detail_code = serializers.IntegerField(allow_null=True, required=False)
#
#     class Meta:
#         model = ClientAddressLookup
#         fields = (
#             "property_address_full",
#             "session_id",