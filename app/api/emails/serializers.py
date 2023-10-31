from rest_framework import serializers

from app.api.email_templates.serializers import EmailTemplateSerializers
from app.api.emails.models import UserEmail
from app.api.projects.serializers import CompanyAccountSerializer, ProjectSerializer
from app.api.users.serializers import UserSerializer


class SendEmailSerializer(serializers.ModelSerializer):

    template = EmailTemplateSerializers(read_only=True)
    user = UserSerializer(read_only=True)
    account = CompanyAccountSerializer(read_only=True)
    contact = CompanyAccountSerializer(read_only=True)
    project = ProjectSerializer(source='opportunity', read_only=True)
    email_type = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = UserEmail
        fields = ('template', 'user', 'account', 'contact', 'project', 'region',
                  'is_mass_email', 'email_type', 'body', 'subject')

        extra_kwargs = {
            'body': {'required': True},
            'subject': {'required': True},
        }

