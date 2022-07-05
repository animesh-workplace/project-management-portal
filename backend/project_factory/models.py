from django.db import models
from .abstract import TableSchema, FieldSchema
from .config import project_app_label, metadata_app_label


class ProjectSchema(TableSchema):
    @property
    def app_label(self):
        return project_app_label()


class ProjectFieldSchema(FieldSchema):
    model_schema = models.ForeignKey(
        ProjectSchema, on_delete=models.CASCADE, related_name="fields"
    )


class MetadataSchema(TableSchema):
    @property
    def app_label(self):
        return metadata_app_label()


class MetadataFieldSchema(FieldSchema):
    model_schema = models.ForeignKey(
        MetadataSchema, on_delete=models.CASCADE, related_name="fields"
    )
