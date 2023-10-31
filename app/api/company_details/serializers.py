from rest_framework import serializers
from .models import BasicCompany, CompanyInfo, Socials, OrgDetails, ProjectHistory, CurrentWork, Insurance, Safety, \
    Finance, Supplier, Legal, ShippingReceivings, CompletedWork


class BasicCompanySerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(write_only=True)

    class Meta:
        model = BasicCompany
        exclude = ('user',)  # Exclude the 'user' field from the serializer fields

    def create(self, validated_data):
        userId = validated_data.pop('userId', None)
        instance = BasicCompany.objects.create(**validated_data)  # Pass validated_data without user_id
        instance.user_id = userId  # Set the user_id separately
        instance.save()
        return instance


class CompanyInfoSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(write_only=True)

    class Meta:
        model = CompanyInfo
        exclude = ('user',)  # Exclude the 'user' field from the serializer fields

    def create(self, validated_data):
        userId = validated_data.pop('userId', None)
        instance = CompanyInfo.objects.create(**validated_data)  # Pass validated_data without user_id
        instance.user_id = userId  # Set the user_id separately
        instance.save()
        return instance


class SocialsSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(write_only=True)

    class Meta:
        model = Socials
        exclude = ('user',)  # Exclude the 'user' field from the serializer fields

    def create(self, validated_data):
        userId = validated_data.pop('userId', None)
        instance = Socials.objects.create(**validated_data)  # Pass validated_data without user_id
        instance.user_id = userId  # Set the user_id separately
        instance.save()
        return instance


class OrgDetailsSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrgDetails
        exclude = ('user',)  # Exclude the 'user' field from the serializer fields

    def create(self, validated_data):
        userId = validated_data.pop('userId', None)
        instance = OrgDetails.objects.create(**validated_data)  # Pass validated_data without user_id
        instance.user_id = userId  # Set the user_id separately
        instance.save()
        return instance


class ProjectHistorySerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(write_only=True)

    class Meta:
        model = ProjectHistory
        exclude = ('user',)  # Exclude the 'user' field from the serializer fields

    def create(self, validated_data):
        userId = validated_data.pop('userId', None)
        instance = ProjectHistory.objects.create(**validated_data)  # Pass validated_data without user_id
        instance.user_id = userId  # Set the user_id separately
        instance.save()
        return instance


class CurrentWorkSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(write_only=True)

    class Meta:
        model = CurrentWork
        exclude = ('user',)  # Exclude the 'user' field from the serializer fields

    def create(self, validated_data):
        userId = validated_data.pop('userId', None)
        instance = CurrentWork.objects.create(**validated_data)  # Pass validated_data without user_id
        instance.user_id = userId  # Set the user_id separately
        instance.save()
        return instance


class CompletedWorkSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(write_only=True)

    class Meta:
        model = CompletedWork
        exclude = ('user',)  # Exclude the 'user' field from the serializer fields

    def create(self, validated_data):
        userId = validated_data.pop('userId', None)
        instance = CompletedWork.objects.create(**validated_data)  # Pass validated_data without user_id
        instance.user_id = userId  # Set the user_id separately
        instance.save()
        return instance


class InsuranceSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(write_only=True)

    class Meta:
        model = Insurance
        exclude = ('user',)  # Exclude the 'user' field from the serializer fields

    def create(self, validated_data):
        userId = validated_data.pop('userId', None)
        instance = Insurance.objects.create(**validated_data)  # Pass validated_data without user_id
        instance.user_id = userId  # Set the user_id separately
        instance.save()
        return instance


class SafetySerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(write_only=True)

    class Meta:
        model = Safety
        exclude = ('user',)  # Exclude the 'user' field from the serializer fields

    def create(self, validated_data):
        userId = validated_data.pop('userId', None)
        instance = Safety.objects.create(**validated_data)  # Pass validated_data without user_id
        instance.user_id = userId  # Set the user_id separately
        instance.save()
        return instance


class FinanceSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(write_only=True)

    class Meta:
        model = Finance
        exclude = ('user',)  # Exclude the 'user' field from the serializer fields

    def create(self, validated_data):
        userId = validated_data.pop('userId', None)
        instance = Finance.objects.create(**validated_data)  # Pass validated_data without user_id
        instance.user_id = userId  # Set the user_id separately
        instance.save()
        return instance


class SupplierSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(write_only=True)

    class Meta:
        model = Supplier
        exclude = ('user',)  # Exclude the 'user' field from the serializer fields

    def create(self, validated_data):
        userId = validated_data.pop('userId', None)
        instance = Supplier.objects.create(**validated_data)  # Pass validated_data without user_id
        instance.user_id = userId  # Set the user_id separately
        instance.save()
        return instance


class LegalSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(write_only=True)

    class Meta:
        model = Legal
        exclude = ('user',)  # Exclude the 'user' field from the serializer fields

    def create(self, validated_data):
        userId = validated_data.pop('userId', None)
        instance = Legal.objects.create(**validated_data)  # Pass validated_data without user_id
        instance.user_id = userId  # Set the user_id separately
        instance.save()
        return instance


class ShippingReceivingsSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(write_only=True)

    class Meta:
        model = ShippingReceivings
        exclude = ('user',)  # Exclude the 'user' field from the serializer fields

    def create(self, validated_data):
        userId = validated_data.pop('userId', None)
        instance = ShippingReceivings.objects.create(**validated_data)  # Pass validated_data without user_id
        instance.user_id = userId  # Set the user_id separately
        instance.save()
        return instance
