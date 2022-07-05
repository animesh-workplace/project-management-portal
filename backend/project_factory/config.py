from django.conf import settings
from .apps import ProjectFactoryConfig, MetadataFactoryConfig


def project_app_label():
    return _settings().get("USE_APP_LABEL", ProjectFactoryConfig.name)


def metadata_app_label():
    return _settings().get("USE_APP_LABEL", MetadataFactoryConfig.name)


def default_fields():
    return _settings().get("DEFAULT_FIELDS", {})


def default_charfield_max_length():
    return _settings().get("DEFAULT_CHARFIELD_MAX_LENGTH", 255)


def cache_key_prefix():
    return _settings().get("CACHE_KEY_PREFIX", "projects_schema_")


def cache_timeout():
    default_timeout = 60 * 60 * 24  # 24 hours
    return _settings().get("CACHE_TIMEOUT", default_timeout)


def _settings():
    return getattr(settings, "projects", {})
