from django.db import models

# Create your models here.
class ProjectHandler(models.Model):
    config = models.JSONField()
    name = models.CharField(max_length=255)
    table_name = models.CharField(max_length=255, primary_key=True)
    # Add timestamp for creation and updation


class MetadataHandler(models.Model):
    config = models.JSONField()
    name = models.CharField(max_length=255)
    table_name = models.CharField(max_length=255, primary_key=True)
    project_name = models.ForeignKey(ProjectHandler, on_delete=models.CASCADE)
    # Add timestamp for creation and updation
