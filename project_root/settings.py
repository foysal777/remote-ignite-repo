from decouple import config
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

# --------------------------------------------------
# ENV
# --------------------------------------------------

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------
# AWS SECRETS
# --------------------------------------------------

import os
from .aws_secrets import load_aws_secrets

aws_secrets = load_aws_secrets("prod/senses", region_name="us-east-2")

OPENAI_API_KEY = aws_secrets.get("OPENAI_API_KEY", "")
PINECONE_API_KEY = aws_secrets.get("PINECONE_API_KEY", "")
ELEVENLABS_API_KEY = aws_secrets.get("ELEVENLABS_API_KEY", "").strip()
STRIPE_SECRET_KEY = aws_secrets.get("STRIPE_SECRET_KEY", "")
STRIPE_PREMIUM_PRICE_ID = aws_secrets.get("STRIPE_PREMIUM_PRICE_ID", "")
STRIPE_TOPUP_PRICE_ID = aws_secrets.get("STRIPE_TOPUP_PRICE_ID", "")
STRIPE_WEBHOOK_SECRET = aws_secrets.get("STRIPE_WEBHOOK_SECRET", "")


# Export for external SDKs
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["ELEVENLABS_API_KEY"] = ELEVENLABS_API_KEY
os.environ["STRIPE_SECRET_KEY"] = STRIPE_SECRET_KEY
os.environ["STRIPE_WEBHOOK_SECRET"] = STRIPE_WEBHOOK_SECRET
os.environ["STRIPE_PREMIUM_PRICE_ID"] = STRIPE_PREMIUM_PRICE_ID
os.environ["STRIPE_TOPUP_PRICE_ID"] = STRIPE_TOPUP_PRICE_ID

PINECONE_INDEX_NAME= os.getenv("PINECONE_INDEX_NAME", "")
print("stripe key :", os.environ.get("STRIPE_SECRET_KEY"))
print("pinecone key :", os.environ.get("STRIPE_WEBHOOK_SECRET"))
print("elevenlabs key :", os.environ.get("ELEVENLABS_API_KEY"))
# --------------------------------------------------
# SECURITY (PRODUCTION)
# --------------------------------------------------

SECRET_KEY = config("SECRET_KEY", default="unsafe-secret")

DEBUG = False   # ✅ MUST be False in production

ALLOWED_HOSTS = [
    "xccess.sensesagi.app",
]

# --------------------------------------------------
# APPLICATIONS
# --------------------------------------------------

INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "channels",

    "accounts",
    "chatbot",
    "subscriptions",

    "rest_framework",
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
     
}

AUTH_USER_MODEL = "accounts.User"
CORS_ALLOW_CREDENTIALS = True

# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",   # MUST be first
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --------------------------------------------------
# PROXY / COOKIE (HTTPS + NGINX)
# --------------------------------------------------

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SAMESITE = "None"

# --------------------------------------------------
# CORS / CSRF
# --------------------------------------------------

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:7006",
    "https://sensesai.app",
    "https://resplendent-figolla-685e32.netlify.app",
    "https://admirable-travesseiro-c07865.netlify.app",
]

CSRF_TRUSTED_ORIGINS = [
    "https://xccess.sensesagi.app",
    "https://sensesai.app",
    "https://resplendent-figolla-685e32.netlify.app",
    "https://admirable-travesseiro-c07865.netlify.app",
]

# --------------------------------------------------
# CORS HEADERS (VERY IMPORTANT)
# --------------------------------------------------

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# --------------------------------------------------
# DATABASE (POSTGRES ON EC2)
# --------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT", cast=int),
    }
}

# --------------------------------------------------
# REDIS / CELERY
# --------------------------------------------------

CELERY_BROKER_URL = config("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [CELERY_BROKER_URL],
        },
    }
}

# --------------------------------------------------
# EMAIL
# --------------------------------------------------

EMAIL_BACKEND = config("EMAIL_BACKEND")
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
ELEVENLABS_AGENT_ID = config('AGENT_ID')

# --------------------------------------------------
# JWT
# --------------------------------------------------

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# --------------------------------------------------
# URL / ASGI / WSGI
# --------------------------------------------------

ROOT_URLCONF = "project_root.urls"
WSGI_APPLICATION = "project_root.wsgi.application"
ASGI_APPLICATION = "project_root.asgi.application"

# --------------------------------------------------
# TEMPLATES
# --------------------------------------------------

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
    }
]

# --------------------------------------------------
# STATIC & MEDIA
# --------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

