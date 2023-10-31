from rest_framework import serializers
from .models import capability_statement


class capabilityStatementSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(write_only=True)

    class Meta:
        model = capability_statement
        exclude = ('user',)  # Exclude the 'user' field from the serializer fields

    def create(self, validated_data):
        userId = validated_data.pop('userId', None)
        instance = capability_statement.objects.create(**validated_data)  # Pass validated_data without user_id
        instance.user_id = userId  # Set the user_id separately
        instance.save()
        return instance
