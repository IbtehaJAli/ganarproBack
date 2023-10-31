from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.api.projects.models import ContactRole


class ContactRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactRole
        fields = ('id', 'contact_role_id', 'contact_id', 'name', 'email', 'phone')
