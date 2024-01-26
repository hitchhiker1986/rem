from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


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
    serial = models.CharField(max_length=30)
    current = models.FloatField()
    delta = models.FloatField(default=0.0)
    dict_start_day = models.PositiveIntegerField(default=1)
    dict_end_day = models.PositiveIntegerField(default=7)
    provider = models.TextField(default="")
    # photo = models.ImageField()

    class Type(models.TextChoices):
        HOTWATER = "HWA", "hot water"
        COLDWATER = "CWA", "cold water"
        ELECTRICITY = "ELE", "electricity"
        GAS = "GAS", "gas"

    class Unit(models.TextChoices):
        KWH = "KWH", "kWh"
        M3 = "M3", "m3"

    type = models.CharField(
        max_length=3,
        choices=Type.choices,
        default='ELE'
        )

    unit = models.CharField(
        max_length=3,
        choices=Unit.choices,
        default='KWH'
    )

    def __str__(self):
        return self.serial

    def set_delta(self, num):
        self.delta = num

    def set_current(self, num):
        self.current = num

    def set_unit(self):
        if self.type == "ELE":
            self.unit = 'KWH'
        else:
            self.unit = 'M3'

    def update_meter(self, new_current):
        self.delta = new_current - self.current
        self.current = new_current

    def get_current(self):
        return self.current

    def get_serial(self):
        return self.serial


class Apartment(models.Model):
    address = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    owner = models.ManyToManyField(Owner, related_name="apartment_owner")
    tenant = models.ManyToManyField(Tenant, related_name="apartment_tenant")
    price = models.PositiveIntegerField(default=0)
    deposit = models.PositiveIntegerField(default=0)
    overhead = models.PositiveIntegerField(default=0)
    premiumPercentage = models.PositiveIntegerField(default=15,
                                                    validators=[MinValueValidator(0), MaxValueValidator(100)])
    premium = models.FloatField(default=0,
                                validators=[MinValueValidator(15000), MaxValueValidator(50000)])
    utilities = models.ManyToManyField(Utility)

    def __str__(self):
        return self.address

    def calculate_premium(self):
        calculated = (int(self.price) / 100) * int(self.premiumPercentage)
        if calculated > 50000:
            return 50000
        elif calculated < 15000:
            return 15000
        else:
            return calculated


class ToDo(models.Model):
    start_day = models.PositiveIntegerField(default=1,)
    end_day = models.PositiveIntegerField(default=1,)
    description = models.TextField(max_length=500,)
    title = models.TextField(max_length=50, )
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, )

    def __str__(self):
        return self.title


class DictHistory(models.Model):
    utility_serial = models.CharField(max_length=30)
    dict_date = models.DateField(auto_now_add=True)
    dict_value = models.FloatField()

    def update_serial(self, serial):
        self.utility_serial = serial

    def update_value(self, value):
        self.dict_date = value


class PaymentHistory(models.Model):
    payment_date = models.DateField(auto_now_add=True)
    payment_amount = models.FloatField(default=0)
    payment_currency = models.CharField(max_length=3)
    payment_owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
