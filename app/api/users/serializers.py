import uuid

import cloudinary.uploader
from django.utils.text import slugify
from rest_framework import serializers
from djstripe.models import Subscription
from rest_framework.fields import SerializerMethodField

from app.api.authentication.models.user_registration import UserProfile, User
from app.api.gc_planify.models import GeneralContractor
from app.api.projects.models import Opportunity
from app.api.projects.serializers import ProjectSerializer


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email')
    customer = serializers.CharField(source='customer.id', default=None, allow_blank=True, allow_null=True)
    subscriptions = SerializerMethodField()
    project_favorites = ProjectSerializer(many=True, read_only=True)
    project_archives = ProjectSerializer(many=True, read_only=True)
    project_viewed = ProjectSerializer(many=True, read_only=True)
    user_type = serializers.SerializerMethodField(source='user.user_type')
    def get_user_type(self, obj):
        return obj.user.get_user_type_display()

    def get_subscriptions(self, obj):
        try:
            subscriptions = SubscriptionSerializer(Subscription.objects.filter(customer_id=obj.customer),
                                                   many=True).data
        except Subscription.DoesNotExist:
            subscriptions = []
        return subscriptions

    class Meta:
        model = UserProfile
        fields = ('id', 'first_name', 'last_name', 'phone', 'address',
                  'email', 'company_name', 'company_state', 'company_street', 'company_zip',
                  'company_contact_name', 'company_contact_phone', 'company_contact_email', 'company_city', 'image',
                  'file_url', "proposal_point_contact_name", "proposal_point_contact_phone",
                  "proposal_point_contact_email",
                  "job_site_contact_name", "job_site_contact_phone", "job_site_contact_email", "free_template_count",
                  "customer", "subscriptions", "free_mode_action", "project_favorites", "project_archives", "project_viewed",
                  "is_domain_verify", "outbound_email", "user_type")

        read_only_fields = ('file_url',)

    def update(self, instance, validated_data):
        user = validated_data.pop('user')
        file_url = None
        image = validated_data.get('image', None)
        if image is not None:
            file_name = validated_data['image'].name
            upload_data = cloudinary.uploader.upload(image)
            file_url = upload_data['secure_url']
            validated_data['file_url'] = file_url
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.outbound_email = validated_data.get('outbound_email', instance.outbound_email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.address = validated_data.get('address', instance.address)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.company_state = validated_data.get('company_state', instance.company_state)
        instance.company_street = validated_data.get('company_street', instance.company_street)
        instance.company_zip = validated_data.get('company_zip', instance.company_zip)
        instance.company_city = validated_data.get('company_city', instance.company_city)
        instance.company_contact_name = validated_data.get('company_contact_name', instance.company_contact_name)
        instance.company_contact_phone = validated_data.get('company_contact_phone', instance.company_contact_phone)
        instance.company_contact_email = validated_data.get('company_contact_email', instance.company_contact_email)
        instance.proposal_point_contact_name = validated_data.get('proposal_point_contact_name',
                                                                  instance.proposal_point_contact_name)
        instance.proposal_point_contact_email = validated_data.get('proposal_point_contact_email',
                                                                   instance.proposal_point_contact_email)
        instance.proposal_point_contact_phone = validated_data.get('proposal_point_contact_phone',
                                                                   instance.proposal_point_contact_phone)
        instance.job_site_contact_name = validated_data.get('job_site_contact_name', instance.job_site_contact_name)
        instance.job_site_contact_phone = validated_data.get('job_site_contact_phone', instance.job_site_contact_phone)
        instance.job_site_contact_email = validated_data.get('job_site_contact_email', instance.job_site_contact_email)
        instance.file_url = validated_data.get('file_url', instance.file_url)
        instance.save()

        # UserProfile.objects.filter(user=instance.user_id).update(**validated_data)
        return instance


class UserSerializer(serializers.ModelSerializer):
    pass
    # profile = UserProfileSerializer(read_only=True)
    #
    # class Meta:
    #     model = User
    #     fields = ('id',
    #               'email',
    #               'profile',
    #               'first_name',
    #               'last_name',
    #               'phone',
    #               )
    #
    # # def create(self, validated_data):
    # #     profile_data = validated_data.pop('user_profile')
    # #
    # #     password = validated_data.pop('password')
    # #
    # #     user = User(**validated_data)
    # #     user.set_password(password)
    # #     user.save()
    # #
    # #     UserProfile.objects.create(user=user, **profile_data)
    # #
    # #     return user
    #
    # def update(self, instance, validated_data):
    #     print('validated_data', validated_data)
    #     file_name = None
    #     file_url = None
    #     note = validated_data['note']
    #     comment_type = validated_data['type']
    #     account_id = self.context['account_id']
    #     project_id = self.context['project_id']
    #     image = validated_data.get('file', None)
    #     if image is not None:
    #         file_name = validated_data['image'].name
    #         upload_data = cloudinary.uploader.upload(image)
    #         file_url = upload_data['secure_url']
    #     profile_data = validated_data.pop('profile')
    #     profile = dict(profile_data)
    #     print(profile)
    #
    #     UserProfile.objects.filter(pk=instance.profile.id).update(**profile)
    #
    #     return instance


class RegisterUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    company_name = serializers.CharField(required=False)
    is_gc = serializers.BooleanField(required=False)
    working_region = serializers.JSONField(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password',
                  'first_name', 'last_name', 'phone', "address", "user_type", "is_gc", "company_name", "working_region")

        extra_kwargs = {'password': {'write_only': True}, 'email': {'required': True, 'allow_blank': False},
                        'confirm_password': {'required': True, 'allow_blank': False},
                        'address': {'required': False, 'allow_blank': True},
                        'phone': {'required': False, 'allow_blank': True}}

    def validate_email(self, email):
        try:
            User.objects.get(email=email.lower())
        except User.DoesNotExist:

            return email.lower()

        raise serializers.ValidationError("Someone with that email "
                                          "address has already registered. Was it you?")

    # def validate_username(self, username):
    #     if User.objects.filter(username=username).exists():
    #         raise serializers.ValidationError('username already exist')
    #     return username

    def create(self, validated_data):
        user_type = "CLN"
        if validated_data.get('is_gc', False):
            user_type = "GC"
            company_name = validated_data.get('company_name')
            if company_name is None:
                raise serializers.ValidationError({"company_name":["company is required"]})

        user = User.objects.create(
            email=validated_data['email'],
            user_type=user_type
        )
        user.set_password(validated_data['password'])
        user.save()
        # create profile
        if validated_data.get('is_gc', False):
            unique_string = uuid.uuid4().hex[:6].upper()
            company_name = validated_data.get('company_name')

            general_contractor = GeneralContractor.objects.create(
                user=user,
                first_name=validated_data.get('first_name'),
                last_name=validated_data.get('last_name'),
                company_name=company_name,
                company_slug=slugify(f"{company_name} {unique_string}"),
                phone=validated_data.get('phone'),
                working_region=validated_data.get('working_region')
            )

            general_contractor.email = validated_data['email']
            return general_contractor

        else:
            user_profile = UserProfile.objects.create(
                user=user,
                first_name=validated_data.get('first_name'),
                last_name=validated_data.get('last_name'),
                phone=validated_data.get('phone'),
                address=validated_data.get('address'),
                outbound_email=validated_data['email'],
            )
            user_profile.email = validated_data['email']
            return user_profile
