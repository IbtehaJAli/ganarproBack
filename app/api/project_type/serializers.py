from rest_framework import serializers

from app.api.authentication.models import User
from app.api.project_type.models import ProjectType
from app.api.proposal.models import Proposal
from app.api.users.serializers import UserSerializer, UserProfileSerializer


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = '__all__'
