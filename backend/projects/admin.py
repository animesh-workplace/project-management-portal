from django.contrib import admin
from projects.models import Projectname, ModelSchema

# Register your models here.
models = Projectname.objects.all()
for model in models:
    reg_model = ModelSchema.objects.get(name=model.modelname).as_model()
    admin.site.register(reg_model)
