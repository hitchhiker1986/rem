from enum import IntEnum

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


# Create your models here.

class Owner(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, )
    name = models.CharField(max_length=50, default="")
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
        return self.name


class Tenant(models.Model):
    #   berlo dokumentumai
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
    # szerzodesek: kikuldott, alairt, kikoltozesi nyilatkozat, atadas-atveteli jk checklista gyerek eseten befogado nyilatkozat, egyeb[]
    address = models.CharField(max_length=30)
    zip = models.IntegerField(blank=False, null=False, default=0)
    district = models.CharField(max_length=6, default="")
    topographical_nr = models.CharField(max_length=20, blank=True)
    floor = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=30)
    owner = models.ManyToManyField(Owner, related_name="apartment_owner")
    tenant = models.ManyToManyField(Tenant, related_name="apartment_tenant")
    size = models.IntegerField(blank=False, default=0)
    rooms = models.IntegerField(blank=False, default=1)
    halfrooms = models.IntegerField(blank=False, default=0)
    balcony_size = models.FloatField(blank=False, default=0.0)
    furnished = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    price = models.PositiveIntegerField(default=0)
    currency = models.TextChoices('HUF', 'EUR')
    deposit = models.PositiveIntegerField(default=0)
    overhead = models.PositiveIntegerField(default=0)
    premiumPercentage = models.PositiveIntegerField(default=15,
                                                    validators=[MinValueValidator(0), MaxValueValidator(100)])
    premium = models.FloatField(default=0,
                                validators=[MinValueValidator(15000), MaxValueValidator(50000)])
    utilities = models.ManyToManyField(Utility, blank=True)
    next_check = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(12)])
    check_status = models.BooleanField(default=True)
    last_check = models.DateField(blank=True, null=True)
    # history = models.ManyToManyField(ContractHistory, related_name="apartment_history", blank=True, null=True)
    # check_history = models.ManyToManyField(CheckHistory, related_name="apartment_check_history", blank=True, null=True)

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


class ContractHistory(models.Model):
    apt = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        null=True,
        related_name='Contracthistory_Apartment',
    )
    start_date = models.DateField(auto_now_add=False)
    end_date = models.DateField(auto_now_add=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

class CheckHistory(models.Model):
    apt = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        null=True,
        related_name='Checkhistory_Apartment',
    )
    checkDate = models.DateField(auto_now_add=True)
    cleaning = models.BooleanField(default=False)
    smoke = models.BooleanField(default=False)
    damage = models.BooleanField(default=False)
    animal = models.BooleanField(default=False)
    equipment_damage = models.BooleanField(default=False)
    not_allowed_tenants = models.BooleanField(default=False)
    description = models.TextField(max_length=500, default=False)

class Deposit(models.Model):
        deposit_status = models.TextChoices("deposit_status", "NOTPAID PARTIALLYPAID PAID NOTRETURNED RETURNED")
        amount = models.FloatField(default=0)


class ToDo(models.Model):
    # status ami alapjan kiertekelodik hogy kihez milyen gyakran kell menni (problemas-e)
    start_day = models.DateField()
    end_day = models.DateField()
    description = models.TextField(max_length=500,)
    title = models.TextField(max_length=50, )
    responsible = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='responsible_user',
    )

    def __str__(self):
        return self.title


class DictHistory(models.Model):
    utility_serial = models.CharField(max_length=30)
    dict_date = models.DateField(auto_now_add=True)
    dict_value = models.FloatField()

    @classmethod
    def update_serial(self, serial):
        self.utility_serial = serial

    @classmethod
    def update_value(self, value):
        self.dict_date = value


class Payment(models.Model):
    due_date = models.DateField()
    payment_date = models.DateField(auto_now_add=True)
    payment_amount = models.FloatField(default=0)
    payment_currency = models.CharField(max_length=3)
    # payment_owner = models.ForeignKey(Owner, on_delete=models.CASCADE, default=Owner.objects.first())
    payment_status = models.TextChoices("payment_status", "PENDING ACTIVE PARTIALLYCOMPLETED COMPLETED")


class Due(models.Model):
    description = models.TextField(max_length=500)
    amount = models.FloatField(blank=False, null=False)
    # apt = models.ForeignKey(Apartment, on_delete=models.CASCADE, default=Apartment.objects.first())


class PaymentBill(models.Model):
    serial = models.CharField(max_length=8, blank=False, null=False)
    date = models.DateField(auto_now_add=True)
    issuer = models.CharField(max_length=30, blank=False, null=False)
    issuer_name = models.CharField(max_length=50, blank=False, null=False)
    issuer_address = models.CharField(max_length=50, blank=False, null=False)
    issuer_tax_nr = models.CharField(max_length=20, blank=False, null=False)
    buyer_name = models.CharField(max_length=50, blank=False, null=False)
    buyer_address = models.CharField(max_length=50, blank=False, null=False)
    sum_amount = models.FloatField()
    amount_text = models.CharField(max_length=50, default="")
    cashier = models.CharField(max_length=30, blank=False, null=False)
    based_on = models.TextChoices("based_on", "Számla Melléklet")


class Bill(models.Model):
    payment_bill = models.ForeignKey(
        PaymentBill,
        null=True,
        on_delete=models.CASCADE,
        related_name='bills')
    bill_number = models.CharField(max_length=20, blank=False, null=False)
    amount = models.FloatField(blank=False, null=False)



# kauciokassza, ami be lett fizetve, amivel tartoznak, ami vissza lett adva, dupla kaucio berlovaltasnal



