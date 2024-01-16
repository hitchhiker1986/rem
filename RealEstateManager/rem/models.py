from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# Create your models here.


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=4)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    birth_name = models.CharField(max_length=50)
    persID = models.CharField(max_length=20)
    taxID = models.CharField(max_length=15)
    iban = models.CharField(max_length=40)
    is_company = models.BooleanField(default=False)
    active_owner = models.BooleanField(default=True)

    def __str__(self):
        return self.user.last_name + " " + self.user.first_name
       # return self.user.username


class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=4)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    birth_name = models.CharField(max_length=50)
    persID = models.CharField(max_length=20)
    taxID = models.CharField(max_length=15)
    iban = models.CharField(max_length=40)
    is_company = models.BooleanField(default=False)
    active_tenant = models.BooleanField(default=True)

    def __str__(self):
        return self.user.last_name + " " + self.user.first_name

class Utility(models.Model):
    class Type(models.TextChoices):
        HOTWATER = "HWA", "hot water"
        COLDWATER = "CWA", "cold water"
        ELECTRICITY = "ELE", "electricity"
        GAS = "GAS", "gas"

    class Unit(models.TextChoices):
        KWH = "KWH", "kWh"
        M3 = "M3", "m3"
    serial = models.CharField(max_length=30)

    type = models.CharField(
        max_length=3,
        choices=Type.choices,
        default='ELE'
        )
    current = models.FloatField()
    unit = models.CharField(
        max_length=3,
        choices=Unit.choices,
        default='KWH'
    )

#   photo = models.ImageField()
    delta = models.FloatField(default=0.0)

    def __str__(self):
        return self.serial

    def set_delta(self, num):
        self.delta = num

    def set_current(self, num):
        self.current = num

    def set_unit(self):
        if (self.type == "ELE"):
            self.unit = 'KWH'
        else:
            self.unit = 'M3'

    def update_meter(self, new_current):
        self.delta = new_current - self.current
        self.current = new_current

class Apartment(models.Model):
#    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    owner = models.ManyToManyField(Owner, related_name="apartment_owner")
    tenant = models.ManyToManyField(Tenant, related_name="apartment_tenant")
#    owner = models.OneToOneField(Owner, on_delete=models.CASCADE, )
#    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, default=None)
#    tenants = models.ForeignKey(User, on_delete=models.CASCADE, )
    utilities = models.ManyToManyField(Utility)

    def __str__(self):
        return self.address


class ToDo(models.Model):
    start_day = models.PositiveIntegerField(default=1,)
    end_day = models.PositiveIntegerField(default=1,)
    description = models.TextField(max_length=500,)
    title = models.TextField(max_length=50, )
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, )

#    def __init__(self, start_day, end_day, description, title, responsible):
#        self.start_day = start_day
#        self.end_day = end_day
#        self.description = description
#        self.title = title
#         self.responsible = responsible

    def __str__(self):
        return self.title

