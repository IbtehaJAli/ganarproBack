from django.contrib import admin

from app.api.project_type.models import ProjectType


# Register your models here.


class ProjectTypeAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]
    list_display = ['name', 'slug', 'template_a', 'template_b', 'created', 'modified']
    search_fields = ['name']
    list_filter = ('created', 'modified')


admin.site.register(ProjectType, ProjectTypeAdmin)
