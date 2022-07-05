from django.conf import settings
from django.contrib import admin
from django.urls import clear_url_caches
from django.db.utils import IntegrityError
from importlib import import_module, reload
from schema_management.models import ProjectHandler
from project_factory.models import ModelSchema, FieldSchema


def create_project_table(table_name, config):
    # Creating the empty table
    model_schema = ModelSchema.objects.create(name=table_name)

    # Creating fields in the model_schema
    for item in config:
        # Might require a try and catch block
        FieldSchema.objects.create(
            null=item["null"],
            name=item["field"],
            unique=item["unique"],
            max_length=item["maxlen"],
            model_schema=model_schema,
            data_type="character"
            if (item["datatype"] == "radio")
            else item["datatype"],
        )

    # Registering model as a prt of Admin panel
    model = model_schema.as_model()
    admin.site.register(model)
    # Reloading URL path
    reload(import_module(settings.ROOT_URLCONF))
    # Clear the URL cache
    clear_url_caches()
