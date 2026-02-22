from decouple import config
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
from corsheaders.defaults import default_headers

# --------------------------------------------------
# ENV
# --------------------------------------------------

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------
# AWS SECRETS
# --------------------------------------------------

from .aws_secrets import load_aws_secrets


aws_secrets = load_aws_secrets("prod/senses", region_name="us-east-2")

OPENAI_API_KEY = aws_secrets.get("OPENAI_API_KEY", "")
PINECONE_API_KEY = aws_secrets.get("PINECONE_API_KEY", "")
ELEVENLABS_API_KEY = aws_secrets.get("ELEVENLABS_API_KEY", "").strip()
STRIPE_SECRET_KEY = aws_secrets.get("STRIPE_SECRET_KEY", "")
STRIPE_PREMIUM_PRICE_ID = aws_secrets.get("STRIPE_PREMIUM_PRICE_ID", "")
STRIPE_TOPUP_PRICE_ID = aws_secrets.get("STRIPE_TOPUP_PRICE_ID", "")
STRIPE_WEBHOOK_SECRET = aws_secrets.get("STRIPE_WEBHOOK_SECRET", "")

os.environ.update({
    "OPENAI_API_KEY": OPENAI_API_KEY,
    "PINECONE_API_KEY": PINECONE_API_KEY,
    "ELEVENLABS_API_KEY": ELEVENLABS_API_KEY,
    "STRIPE_SECRET_KEY": STRIPE_SECRET_KEY,
    "STRIPE_WEBHOOK_SECRET": STRIPE_WEBHOOK_SECRET,
    "STRIPE_PREMIUM_PRICE_ID": STRIPE_PREMIUM_PRICE_ID,
    "STRIPE_TOPUP_PRICE_ID": STRIPE_TOPUP_PRICE_ID,
})

PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "")

# --------------------------------------------------
# SECURITY
# --------------------------------------------------

SECRET_KEY = config("SECRET_KEY", default="unsafe-secret")
DEBUG = False
ALLOWED_HOSTS = ["*"]

# --------------------------------------------------
# APPLICATIONS
# --------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "channels",
    "accounts",
    "chatbot",
    "subscriptions",
    "rest_framework",
]

AUTH_USER_MODEL = "accounts.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
}


from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),     
    "ROTATE_REFRESH_TOKENS": True,                 
    "BLACKLIST_AFTER_ROTATION": True,                
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),

}

# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # MUST be first
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --------------------------------------------------
# PROXY / HTTPS
# --------------------------------------------------

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = False  # IMPORTANT for CORS preflight (can enable later)

# --------------------------------------------------
# CORS / CSRF (FIXED)
# --------------------------------------------------

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    "https://resplendent-figolla-685e32.netlify.app",
    "https://xccess.sensesagi.app",
    "https://sensesai.app",
]

CORS_ALLOW_HEADERS = list(default_headers) + [
    "authorization",
    "content-type",
    "x-csrftoken",
    "ngrok-skip-browser-warning",
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

CSRF_TRUSTED_ORIGINS = [
    "https://resplendent-figolla-685e32.netlify.app",
    "https://xccess.sensesagi.app",
    "https://sensesai.app",
]


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "us-east-1")
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_DEFAULT_ACL = None 
AWS_S3_VERIFY = True



DATA_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024





SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SAMESITE = "None"



# FireBase Verify Token 

import firebase_admin
from firebase_admin import credentials

FIREBASE_CERT_PATH = os.path.join(BASE_DIR, "firebase-service-account.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CERT_PATH)
    firebase_admin.initialize_app(cred)





# --------------------------------------------------
# DATABASE
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

EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)  
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', cast=bool)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD='072iH3%#'

ELEVENLABS_AGENT_ID = config("AGENT_ID")

# --------------------------------------------------
# JWT
# --------------------------------------------------


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

