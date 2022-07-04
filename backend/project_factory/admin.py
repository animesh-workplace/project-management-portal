from .models import ModelSchema
from django.contrib import admin
from schema_management.models import ProjectHandler

# Register your models here
models = ProjectHandler.objects.all()
for model in models:
    reg_model = ModelSchema.objects.get(name=model.modelname).as_model()
    admin.site.register(reg_model)

admin.site.register(ProjectHandler)
