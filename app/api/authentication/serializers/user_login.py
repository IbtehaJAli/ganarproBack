import json
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import Http404
from djstripe.models import Subscription
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from app.api.authentication.models.user_registration import UserProfile
from app.api.gc_planify.models import GeneralContractor
from app.api.gc_planify.serializers import GeneralContractorsSerializer
from app.api.users.serializers import UserSerializer, UserProfileSerializer

class EmailTokenObtainSerializer(TokenObtainSerializer):
    username_field = User.EMAIL_FIELD


class CustomTokenObtainPairSerializer(EmailTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        # subscription = Subscription.objects.filter(customer=customer_object)
        try:
            User = get_user_model()
            user = User.objects.get(id=self.user.id)
            data["data"] = user.email
            model = UserProfile if user.user_type  == "CLN" else GeneralContractor
            if user.user_type == "CLN":
                user_profile = UserProfile.objects.get(user=self.user)
                data["data"] = UserProfileSerializer(user_profile).data
            else:
                user_profile = GeneralContractor.objects.get(user=self.user)
                data["data"] = GeneralContractorsSerializer(user_profile).data
            return data
        except model.DoesNotExist:
            raise Http404

