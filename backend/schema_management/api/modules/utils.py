from django.utils.text import slugify
from rest_framework import exceptions


def get_name(table_type, user, project, metadata=None):
    if table_type == "project":
        return f"{user}_{slugify(project).replace('-', '_')}_si"
    if table_type == "metadata":
        return f"{user}_{slugify(project).replace('-', '_')}_{slugify(metadata).replace('-', '_')}_metadata"
    raise exceptions.ValidationError("Invalid Type: Get name -> Metadata")
