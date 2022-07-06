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
            name=item["bname"],
            unique=item["unique"],
            required=item["required"],
            model_schema=model_schema,
            data_type=item["data_type"],
            max_length=item["max_length"],
            options=item["options"] if ("options" in item.keys()) else None,
        )
    # Registering model as a prt of Admin panel
    model = model_schema.as_model()
    admin.site.register(model)
    # Reloading URL path
    reload(import_module(settings.ROOT_URLCONF))
    # Clear the URL cache
    clear_url_caches()


def UploadProjectData(project_name, data, app_model):
    obj_list = [app_model(**data_dict) for data_dict in data]
    app_model.objects.bulk_create(obj_list)
    # return Response({"message": "Data uploaded successfully"})
