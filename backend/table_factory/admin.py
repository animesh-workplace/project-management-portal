from .models import TableSchema
from django.contrib import admin
from schema_management.models import ProjectHandler, MetadataHandler

# Register your models here
models = ProjectHandler.objects.all()
for model in models:
    try:
        reg_model = TableSchema.objects.get(name=model.table_name).as_model()
        admin.site.register(reg_model)
    except TableSchema.DoesNotExist:
        print(f"{model.table_name} doesnot exist")

models = MetadataHandler.objects.all()
for model in models:
    try:
        reg_model = TableSchema.objects.get(name=model.table_name).as_model()
        admin.site.register(reg_model)
    except TableSchema.DoesNotExist:
        print(f"{model.table_name} doesnot exist")
