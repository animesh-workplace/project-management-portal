from django.apps import AppConfig


class ProjectFactoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "project_factory"


class MetadataFactoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "metadata_factory"
