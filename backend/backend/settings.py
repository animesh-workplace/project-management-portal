import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load dot files
load_dotenv(BASE_DIR / ".env")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "channels",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
]

LOCAL_APPS = ["authentication", "schema_management", "table_factory"]

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ASGI_APPLICATION = "backend.asgi.application"

# Channel Layers
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "database" / "db.sqlite3",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
USE_TZ = True
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"

# Static files (CSS, JavaScript, Images)
STATIC_URL = f"{os.getenv('BASE_URL')}static/"
STATIC_ROOT = BASE_DIR / "static"

# Media files (CSS, JavaScript, Images)
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = f"{os.getenv('BASE_URL')}media/"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication user model
AUTH_USER_MODEL = "authentication.user"

# REST Framework default authentication and exception handler
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "authentication.api.jwt_auth.JWTCookieAuthentication",
    ],
    # 'EXCEPTION_HANDLER': 'authentication.api.utils.custom_exception_handler'
}

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOWED_ORIGINS = [ 'http://127.0.0.1:3030' ]
# CORS_ALLOWED_ORIGIN_REGEXES = [ 'http://127.0.0.1:3030' ]

# JWT Cookie (auth and refresh) information
JWT_AUTH_SECURE = False
JWT_AUTH_HTTPONLY = True
JWT_AUTH_SAMESITE = "Lax"
JWT_AUTH_COOKIE = "JWT-AUTH"
JWT_AUTH_COOKIE_USE_CSRF = True
JWT_AUTH_LIFETIME = timedelta(hours=6)
JWT_AUTH_REFRESH_COOKIE = "JWT-REFRESH"
JWT_AUTH_REFRESH_LIFETIME = timedelta(days=7)
JWT_AUTH_COOKIE_PATH = f"/{os.getenv('BASE_URL')}"
JWT_AUTH_REFRESH_COOKIE_PATH = f"/{os.getenv('BASE_URL')}"

# CSRF Cookie information
CSRF_USE_SESSIONS = False
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_NAME = "XSRF-TOKEN"
CSRF_HEADER_NAME = "HTTP_X_XSRF_TOKEN"
CSRF_COOKIE_PATH = f"/{os.getenv('BASE_URL')}"
CSRF_TRUSTED_ORIGINS = [os.getenv("TRUSTED_ORIGIN")]

# Session Cookie information
SESSION_COOKIE_PATH = f"/{os.getenv('BASE_URL')}"

# SIMPLE-JWT Settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": JWT_AUTH_LIFETIME,
    "REFRESH_TOKEN_LIFETIME": JWT_AUTH_REFRESH_LIFETIME,
}
