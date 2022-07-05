from django.contrib import admin
from .models import ProjectSchema, MetadataSchema
from schema_management.models import ProjectHandler, MetadataHandler

# Register your models here
models = ProjectHandler.objects.all()
for model in models:
    try:
        reg_model = ProjectSchema.objects.get(name=model.table_name).as_model()
        admin.site.register(reg_model)
    except ProjectSchema.DoesNotExist:
        print(f"{model.table_name} doesnot exist")

models = MetadataHandler.objects.all()
for model in models:
    try:
        reg_model = MetadataSchema.objects.get(name=model.table_name).as_model()
        admin.site.register(reg_model)
    except MetadataSchema.DoesNotExist:
        print(f"{model.table_name} doesnot exist")
