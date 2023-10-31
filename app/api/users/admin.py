from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import User
from ..authentication.models.user_registration import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = 'UserProfile'
    fk_name = 'user'


    # raw_id_fields = ("company_account_favorites", "company_account_archives",
    #                  "contact_favorites", "contact_archives", "company_accounts", "user_regions",
    #                  "hot_scopes")

# class MarketInline(admin.StackedInline):
#     model = Market
#     can_delete = False
#     verbose_name = 'Markets'
#     fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )


    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


class UserProfileAdmin(admin.ModelAdmin):

    list_display  = [field.name for field in UserProfile._meta.fields if field.name != "id"]
    readonly_fields = ('user_email',)
    search_fields = ['first_name', 'last_name', 'user__username', 'user__email']
    list_filter = ('created', 'modified')

    def user_email(self, obj):
        return obj.user.email

# admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

# admin.site.register(Account, SimpleHistoryAdmin)

# SimpleHistoryAdminfrom reversion.admin import VersionAdmin

# @admin.register(Account)
# class AccountAdmin(VersionAdmin):
#     pass