from tkinter.tix import Meter

from django import forms
from .models import Utility, Tenant, Apartment, CheckHistory, Bill, PaymentBill, ToDo
from django.db import models
from django.forms.models import inlineformset_factory, BaseInlineFormSet

class ApartmentCreateForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ('address', 'city', 'zip', 'floor', 'district', 'topographical_nr', 'size', 'balcony_size', 'rooms', 'halfrooms', )


class DictForm(forms.ModelForm):
    class Meta:
        model = Utility
        fields = ('current', )


class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ('country', 'city', 'zip', 'address', 'phone', 'iban', 'active_tenant', )


class CheckForm(forms.ModelForm):
    class Meta:
        model = CheckHistory
        fields = ('cleaning', 'smoke', 'damage', 'animal', 'equipment_damage', 'not_allowed_tenants', 'description',)
    # checkform archivalas, description


# https://micropyramid.com/blog/how-to-use-nested-formsets-in-django
# https://github.com/philgyford/django-nested-inline-formsets-example/blob/main/publishing/books/forms.py

class PaymentBillForm(forms.ModelForm):
    class Meta:
        model = PaymentBill
        fields = ('issuer', 'issuer_name', 'issuer_address', 'issuer_tax_nr', 'buyer_name', 'buyer_address', 'amount_text', 'cashier')


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ('amount', 'bill_number',)


BillAndPaymentBillFormSet = inlineformset_factory(
    PaymentBill, Bill, form = BillForm,
    extra=1, can_delete=True, can_delete_extra=True
)

class SentContractForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ('sent_contract', )


class CreateUtilityForm(forms.ModelForm):
    class Meta:
        model = Utility
        fields = ('__all__')


class task_form(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ('__all__')

    widgets = {
        'start_day': forms.DateInput(),
        'end_day': forms.DateInput(),
    }
