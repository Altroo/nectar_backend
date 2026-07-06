from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY", default="dev-insecure-nectar")
DEBUG = config("DEBUG", default="True", cast=bool)

ALLOWED_HOSTS = [
    host.strip()
    for host in config("ALLOWED_HOSTS", default="127.0.0.1,localhost").split(",")
    if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in config(
        "CSRF_TRUSTED_ORIGINS",
        default="http://127.0.0.1:3008,http://localhost:3008",
    ).split(",")
    if origin.strip()
]

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in config(
        "CORS_ALLOWED_ORIGINS",
        default="http://127.0.0.1:3008,http://localhost:3008",
    ).split(",")
    if origin.strip()
]
CORS_ALLOW_CREDENTIALS = True

SITE_PHONE = config("SITE_PHONE", default="212675599256")
SITE_PHONE_DISPLAY = config(
    "SITE_PHONE_DISPLAY", default="06 75 59 92 56 / 07 73 86 35 85"
)
SITE_EMAIL = config("SITE_EMAIL", default="info@nectar.ma")
SITE_EMAIL_DISPLAY = config("SITE_EMAIL_DISPLAY", default="contact@nectar.ma")
SITE_DEFAULT_LANG = config("SITE_DEFAULT_LANG", default="fr")

EMAIL_BACKEND = config(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default="587", cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default="True", cast=bool)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", default="False", cast=bool)
EMAIL_TIMEOUT = config("EMAIL_TIMEOUT", default="30", cast=int)
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default=SITE_EMAIL)
SERVER_EMAIL = config("SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
CONTACT_NOTIFICATION_EMAILS = [
    email.strip()
    for email in config(
        "CONTACT_NOTIFICATION_EMAILS",
        default=config("CONTACT_REQUEST_RECIPIENT", default="contact@nectar.ma"),
    ).split(",")
    if email.strip()
]
PURPLE_PEARL_VISIT_NOTIFICATION_EMAILS = [
    email.strip()
    for email in config(
        "PURPLE_PEARL_VISIT_NOTIFICATION_EMAILS",
        default=config("PURPLE_PEARL_VISIT_RECIPIENT", default=",".join(CONTACT_NOTIFICATION_EMAILS)),
    ).split(",")
    if email.strip()
]
NEWSLETTER_NOTIFICATION_EMAILS = [
    email.strip()
    for email in config(
        "NEWSLETTER_NOTIFICATION_EMAILS",
        default=config("NEWSLETTER_RECIPIENT", default="info@nectar.ma"),
    ).split(",")
    if email.strip()
]
CONTACT_REQUEST_RECIPIENT = ",".join(CONTACT_NOTIFICATION_EMAILS)
PURPLE_PEARL_VISIT_RECIPIENT = ",".join(PURPLE_PEARL_VISIT_NOTIFICATION_EMAILS)
NEWSLETTER_RECIPIENT = ",".join(NEWSLETTER_NOTIFICATION_EMAILS)

INSTALLED_APPS = [
    "account.apps.AccountConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "website.apps.WebsiteConfig",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "nectar_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "nectar_backend.wsgi.application"
ASGI_APPLICATION = "nectar_backend.asgi.application"

if config("POSTGRES_HOST", default=""):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("POSTGRES_DB", default="nectar"),
            "USER": config("POSTGRES_USER", default="postgres"),
            "PASSWORD": config("POSTGRES_PASSWORD", default=""),
            "HOST": config("POSTGRES_HOST"),
            "PORT": config("POSTGRES_PORT", default="5432"),
            "CONN_MAX_AGE": 0,
            "CONN_HEALTH_CHECKS": True,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "fr"
TIME_ZONE = "Africa/Casablanca"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.CustomUser"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
}
