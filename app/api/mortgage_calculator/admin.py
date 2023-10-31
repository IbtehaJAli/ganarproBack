from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from app.api.mortgage_calculator.models import PricingModel, StateLaborPrice


# Register your models here.
@admin.register(PricingModel)
class PricingModel(ImportExportModelAdmin):
    class Meta:
        model = PricingModel


# Register your models here.
@admin.register(StateLaborPrice)
class StateLaborPrice(ImportExportModelAdmin):
    class Meta:
        model = StateLaborPrice
