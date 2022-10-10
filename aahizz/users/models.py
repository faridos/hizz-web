from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import APIException
from django.conf import settings
from django.contrib import admin


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """Creates and saves a new user"""
        groups = extra_fields.pop('groups', None)
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save()
        if groups:
            for group in groups:
                user.groups.add(group)
        user.save()
        return user

    def create_superuser(self, email, password):

        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

    def _assign_customer_based_permissions(self, user, customer_obj):
        customer_obj.customer_users.add(user)
        customer_obj.save()

        content_type_customer = ContentType.objects.get_for_model(Customer)
        all_prop_permissions = Permission.objects.filter(content_type=content_type_customer)
        for perm in all_prop_permissions:
            assign_perm(perm.codename, user, customer_obj)

        UserCustomerRole.objects.create(customer=customer_obj, user=user, user_type="OWNER")

class User(AbstractBaseUser, PermissionsMixin):
    """User model for auth"""

    email = models.EmailField(max_length=255, unique=True)
    firstname = models.CharField(max_length=255, null=True, default=None)
    surname = models.CharField(max_length=255, null=True, default=None)
    name = models.CharField(max_length=255, null=True, default=None)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(max_length=None, blank=True, null=True, default=None)
    telephone = models.CharField(max_length=20, blank=True, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    # TODO field:
    @property
    def customer_dachb_profile(self):
       pass

    objects = UserManager()

    USERNAME_FIELD = 'email'

admin.site.register(User)