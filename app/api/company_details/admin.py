from django.contrib import admin

# Register your models here.
from .models import BasicCompany, CompanyInfo, Socials, ProjectHistory, CompletedWork, CurrentWork, OrgDetails, \
    Insurance, Safety, Finance, Supplier, Legal, ShippingReceivings

# Register your models here.
admin.site.register(BasicCompany)
admin.site.register(CompanyInfo)
admin.site.register(Socials)
admin.site.register(ProjectHistory)
admin.site.register(CompletedWork)
admin.site.register(CurrentWork)
admin.site.register(OrgDetails)
admin.site.register(Insurance)
admin.site.register(Safety)
admin.site.register(Finance)
admin.site.register(Supplier)
admin.site.register(Legal)
admin.site.register(ShippingReceivings)
