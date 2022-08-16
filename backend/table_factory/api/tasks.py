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


def CreateMetadataTable(table_name, config, project):
    # Creating the empty table
    model_schema = TableSchema.objects.create(name=table_name)
    # Creating fields in the model_schema
    si_config_data = list(
        ProjectHandler.objects.filter(
            table_name=f"{table_name.rsplit('_',2)[0]}_si"
        ).values_list("config", flat=True)
    )[0]
    si_config_data_object = next(
        filter(lambda i: i["unique"] == "True", si_config_data)
    )
    print(si_config_data_object["name"])
    FieldSchema.objects.create(
        null=False,
        name=f"{si_config_data_object['name']}_id",
        unique=True,
        max_length=225,
        model_schema=model_schema,
        data_type="character",
    )
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


def UploadData(project_name, data, app_model):
    obj_list = [app_model(**data_dict) for data_dict in data]
    app_model.objects.bulk_create(obj_list)
    # return Response({"message": "Data uploaded successfully"})


def UpdateData(project_name, data, app_model, id):
    obj_list = [app_model(**data_dict) for data_dict in data]
    app_model.objects.filter(id=id).update(**data[0])
