from django.conf import settings
from django.contrib import admin
from django.urls import clear_url_caches
from django.db.utils import IntegrityError
from importlib import import_module, reload
from ..models import TableSchema, FieldSchema
from schema_management.models import ProjectHandler


def CreateTable(table_name, config):
    # Creating the empty table
    model_schema = TableSchema.objects.create(name=table_name)
    # Creating fields in the model_schema
    for item in config:
        # Might require a try and catch block
        FieldSchema.objects.create(
            null=item["null"],
            name=item["name"],
            unique=item["unique"],
            max_length=item["max_length"],
            model_schema=model_schema,
            data_type="character"
            if (item["data_type"] == "radio")
            else item["data_type"],
        )
    # Registering model as a prt of Admin panel
    model = model_schema.as_model()
    admin.site.register(model)
    # Reloading URL path
    reload(import_module(settings.ROOT_URLCONF))
    # Clear the URL cache
    clear_url_caches()
