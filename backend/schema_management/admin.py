from django.contrib import admin
from .models import MetadataHandler, ProjectHandler


# Register your models here
class ProjectHandlerAdmin(admin.ModelAdmin):
    list_display = ("name", "table_name")
    fields = ("name", "table_name", "config")


class MetadataHandlerAdmin(admin.ModelAdmin):
    list_display = ("name", "project_name", "table_name")
    fields = ("name", "project_name", "table_name", "config")


admin.site.register(ProjectHandler, ProjectHandlerAdmin)
admin.site.register(MetadataHandler, MetadataHandlerAdmin)
