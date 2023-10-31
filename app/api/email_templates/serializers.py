from rest_framework import serializers
from .models import EmailTemplate


class EmailTemplateSerializers(serializers.ModelSerializer):

    class Meta:
        model = EmailTemplate
        fields = ('id', 'name',)
