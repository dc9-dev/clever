from audioop import reverse
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.urls import reverse
from django.db import models
from decimal import Decimal


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, first_name, password, **other_fields)

    def create_user(self, email, first_name, password, **other_fields):

        other_fields.setdefault('is_active', True)

        if not email:
            raise ValueError('Email jest wymagany')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class UserBase(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    # Delivery details
    phone_number = models.CharField(max_length=15, blank=True)
    postcode = models.CharField(max_length=12, blank=True)
    address_line_1 = models.CharField(max_length=150, blank=True)
    address_line_2 = models.CharField(max_length=150, blank=True)
    town_city = models.CharField(max_length=150, blank=True)
    # User Status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = "Konto"
        verbose_name_plural = "Konta"

    def __str__(self):
        return ("{} {}".format(self.first_name, self.last_name))
    
    def get_full_name(self):
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()



class Customer(models.Model):

    email = models.EmailField(unique=True, blank=True)
    company = models.CharField(max_length=150, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    # Delivery details
    phone_number = models.CharField(max_length=15, blank=True)
    postcode = models.CharField(max_length=12, blank=True)
    address_line_1 = models.CharField(max_length=150, blank=True)
    address_line_2 = models.CharField(max_length=150, blank=True)
    town_city = models.CharField(max_length=150, blank=True)
    balance =  models.DecimalField(default=Decimal('0.00'), decimal_places=2, blank=True, max_digits=10)

    class Meta:
        verbose_name = "Klient"
        verbose_name_plural = "Klienci"

    def __str__(self):
        return self.company

   
    