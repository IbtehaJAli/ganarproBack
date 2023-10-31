from cloudinary.models import CloudinaryField
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from djstripe.models import Subscription, Customer

from app.api.models import TimestampedModel
from app.api.projects.models import Opportunity, SavedSearch


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.
    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, username, email, password=None):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError("Users must have a username.")

        if email is None:
            raise TypeError("Users must have an email address.")

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser powers.
        Superuser powers means that this use is an admin that can do anything
        they want.
        """
        if password is None:
            raise TypeError("Superusers must have a password.")
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    username = models.CharField(
        db_index=True, max_length=255, unique=False, default="default-username"
    )
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False) # a
    CLEANERS = "CLN"
    GENERAL_CONTRACTOR = "GC"
    USER_TYPE = [
        (CLEANERS, "cleaner"),
        (GENERAL_CONTRACTOR, "general_contractor"),
    ]
    # admin user; non super-user
    user_type = models.CharField(default=CLEANERS, blank=False, choices=USER_TYPE, max_length=20)
    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.profile
        This string is used when a `User` is printed in the console.
        """
        return self.email


class UserProfile(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL, related_name='profile')
    subscription = models.ForeignKey(Subscription, null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField('First Name', max_length=50, blank=False)
    last_name = models.CharField('Last Name', max_length=50, blank=False)
    phone = models.CharField(blank=True, null=True, max_length=20)
    company_name = models.CharField(blank=True, null=True, max_length=50, unique=False)
    company_state = models.CharField(blank=True, null=True, max_length=50, unique=False)
    company_street = models.CharField(blank=True, null=True, max_length=200, unique=False)
    company_zip = models.CharField(blank=True, null=True, max_length=13, unique=False)
    company_contact_name = models.CharField(blank=True, null=True, max_length=100, unique=False)
    company_contact_phone = models.CharField(blank=True, null=True, max_length=100, unique=False)
    company_contact_email = models.CharField(blank=True, null=True, max_length=100, unique=False)
    proposal_point_contact_name = models.CharField(blank=True, null=True, max_length=100, unique=False)
    proposal_point_contact_email = models.CharField(blank=True, null=True, max_length=100, unique=False)
    proposal_point_contact_phone = models.CharField(blank=True, null=True, max_length=100, unique=False)
    job_site_contact_name = models.CharField(max_length=150, blank=True, null=True)
    job_site_contact_email = models.CharField(max_length=150, blank=True, null=True)
    job_site_contact_phone = models.CharField(max_length=150, blank=True, null=True)

    company_city = models.CharField(blank=True, null=True, max_length=13, unique=False)
    image = CloudinaryField('image', null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    file_url = models.URLField(null=True, blank=True)
    free_template_count = models.IntegerField(blank=False, null=True, default=2)
    free_mode_action = models.IntegerField(blank=False, null=True, default=0)
    project_favorites = models.ManyToManyField(Opportunity, blank=True, related_name='user_project_favorites')
    project_archives = models.ManyToManyField(Opportunity, blank=True, related_name='user_project_archives')
    project_viewed = models.ManyToManyField(Opportunity, blank=True, related_name='user_project_viewed', default=None)
    saved_searches = models.ManyToManyField(SavedSearch, blank=True, related_name="user_saved_searches", default=None)
    is_domain_verify = models.BooleanField(default=False, null=True)
    domain_verification_date = models.DateTimeField(auto_now_add=True, null=True)
    outbound_email = models.EmailField(null=True, blank=True)

    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return f"{self.first_name} {self.first_name}"

