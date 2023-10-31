from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin


@admin.register(Opportunity)
class PricingModel(ImportExportModelAdmin):
    class Meta:
        model = Opportunity


@admin.register(CompanyAccount)
class Account(ImportExportModelAdmin):
    class Meta:
        model = CompanyAccount
