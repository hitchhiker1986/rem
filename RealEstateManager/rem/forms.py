from django import forms
from .models import Utility, Tenant


class DictForm(forms.ModelForm):
    class Meta:
        model = Utility
        fields = ('current', )
#        new_value = forms.FloatField(label="Uj ertek ")


class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ('country', 'address', )