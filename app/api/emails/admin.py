from django.contrib import admin

from app.api.emails.models import EmailRule, UserEmail


# Register your models here.


class UserEmailAdmin(admin.ModelAdmin):
    list_filter = ('time_sent', 'is_mass_email')
    list_display = ('subject', 'contact', 'opportunity', 'account', 'user', 'time_sent', 'template',
                    'email_type', 'is_mass_email')


class EmailRuleAdmin(admin.ModelAdmin):
    list_display = ('type', 'created')


admin.site.register(EmailRule, EmailRuleAdmin)
admin.site.register(UserEmail, UserEmailAdmin)
