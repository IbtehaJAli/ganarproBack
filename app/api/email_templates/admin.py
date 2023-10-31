from django.contrib import admin

from app.api.email_templates.models import EmailTemplate


# Register your models here.


class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'ordering', 'created_at')


admin.site.register(EmailTemplate, EmailTemplateAdmin)
