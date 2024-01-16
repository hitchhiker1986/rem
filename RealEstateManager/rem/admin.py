from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Apartment)
admin.site.register(Owner)
admin.site.register(Tenant)
admin.site.register(Utility)
admin.site.register(ToDo)
