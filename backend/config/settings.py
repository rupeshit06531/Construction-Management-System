"""
Django settings for config project.
"""

from pathlib import Path
from datetime import timedelta
import logging.config
import os

from dotenv import load_dotenv


# ============================================================
# BASE CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is not configured in the environment."
    )


DEBUG = os.getenv(
    "DEBUG",
    "False",
).strip().lower() == "true"


ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "ALLOWED_HOSTS",
        "",
    ).split(",")
    if host.strip()
]


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    # Django Apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third Party Apps
    "rest_framework",
    "drf_spectacular",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",

    # Local Apps
    "apps.common",
    "apps.accounts",
    "apps.projects",
    "apps.employees",
    "apps.tasks",
    "apps.materials",
    "apps.inventory",
    "apps.attendance",
    "apps.expenses",
    "apps.payroll",
    "apps.reports",
    "apps.dashboard",
]


# ============================================================
# MIDDLEWARE
# ============================================================

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


# ============================================================
# URL / WSGI
# ============================================================

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ============================================================
# DATABASE
# ============================================================

DATABASES = {
    "default": {
        "ENGINE": os.getenv(
            "DB_ENGINE",
            "django.db.backends.sqlite3",
        ),
        "NAME": BASE_DIR / os.getenv(
            "DB_NAME",
            "db.sqlite3",
        ),
    }
}


# ============================================================
# AUTHENTICATION
# ============================================================

AUTH_USER_MODEL = "accounts.User"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = os.getenv(
    "LANGUAGE_CODE",
    "en-us",
)

TIME_ZONE = os.getenv(
    "TIME_ZONE",
    "UTC",
)

USE_I18N = os.getenv(
    "USE_I18N",
    "True",
).strip().lower() == "true"

USE_TZ = os.getenv(
    "USE_TZ",
    "True",
).strip().lower() == "true"


# ============================================================
# STATIC / MEDIA
# ============================================================

STATIC_URL = "static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# DJANGO REST FRAMEWORK
# ============================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],

    "DEFAULT_SCHEMA_CLASS": (
        "drf_spectacular.openapi.AutoSchema"
    ),

    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],

    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],

    "DEFAULT_PAGINATION_CLASS": (
        "apps.common.pagination.StandardResultsSetPagination"
    ),

    "PAGE_SIZE": 20,

    "EXCEPTION_HANDLER": (
        "apps.common.exceptions.custom_exception_handler"
    ),
}


# ============================================================
# OPENAPI / SWAGGER
# ============================================================

SPECTACULAR_SETTINGS = {
    "TITLE": "Construction Management System API",

    "DESCRIPTION": (
        "Enterprise Construction Management System API Documentation"
    ),

    "VERSION": "1.0.0",

    "SERVE_INCLUDE_SCHEMA": False,

    "TAGS": [
        {
            "name": "Accounts",
            "description": (
                "User authentication and profile management APIs"
            ),
        },
        {
            "name": "Projects",
            "description": (
                "Construction project management APIs"
            ),
        },
        {
            "name": "Employees",
            "description": (
                "Employee management APIs"
            ),
        },
        {
            "name": "Tasks",
            "description": (
                "Project task management APIs"
            ),
        },
        {
            "name": "Materials",
            "description": (
                "Material management APIs"
            ),
        },
        {
            "name": "Inventory",
            "description": (
                "Inventory tracking APIs"
            ),
        },
        {
            "name": "Attendance",
            "description": (
                "Employee attendance APIs"
            ),
        },
        {
            "name": "Expenses",
            "description": (
                "Project expense management APIs"
            ),
        },
        {
            "name": "Payroll",
            "description": (
                "Employee payroll APIs"
            ),
        },
        {
            "name": "Reports",
            "description": (
                "System reports APIs"
            ),
        },
        {
            "name": "Dashboard",
            "description": (
                "Dashboard analytics APIs"
            ),
        },
    ],

    "COMPONENT_SPLIT_REQUEST": True,
}


# ============================================================
# JWT
# ============================================================

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=30
    ),

    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=7
    ),

    "ROTATE_REFRESH_TOKENS": True,

    "BLACKLIST_AFTER_ROTATION": True,

    "AUTH_HEADER_TYPES": (
        "Bearer",
    ),
}


# ============================================================
# CORS
# ============================================================

CORS_ALLOW_ALL_ORIGINS = os.getenv(
    "CORS_ALLOW_ALL_ORIGINS",
    "False",
).strip().lower() == "true"


# ============================================================
# CSRF
# ============================================================

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CSRF_TRUSTED_ORIGINS",
        "",
    ).split(",")
    if origin.strip()
]


# ============================================================
# SECURITY HEADERS
# ============================================================

SECURE_BROWSER_XSS_FILTER = True

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"


# ============================================================
# PRODUCTION SECURITY
# ============================================================

if DEBUG:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

else:
    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 31536000

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_HSTS_PRELOAD = True


# ============================================================
# LOGGING
# ============================================================

LOGGING_CONFIG = None

from config.logging import LOGGING

logging.config.dictConfig(LOGGING)

