import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-local-only-secret")
DEBUG = os.getenv("DEBUG", "1") == "1"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
INSTALLED_APPS = ["django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes", "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles", "rest_framework", "rest_framework_simplejwt.token_blacklist", "drf_spectacular", "corsheaders", "core"]
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware", "corsheaders.middleware.CorsMiddleware", "django.contrib.sessions.middleware.SessionMiddleware", "django.middleware.common.CommonMiddleware", "django.middleware.csrf.CsrfViewMiddleware", "django.contrib.auth.middleware.AuthenticationMiddleware", "django.contrib.messages.middleware.MessageMiddleware", "django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[],"APP_DIRS":True,"OPTIONS":{"context_processors":["django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION = "config.wsgi.application"
DATABASES = {"default": {"ENGINE":"django.db.backends.postgresql","NAME":os.getenv("DB_NAME", "app"),"USER":os.getenv("POSTGRES_USER", "marketplace"),"PASSWORD":os.getenv("POSTGRES_PASSWORD", "local-dev-only-change-me"),"HOST":os.getenv("DB_HOST", "localhost"),"PORT":os.getenv("DB_PORT", "5432"),"CONN_MAX_AGE":60}}
AUTH_PASSWORD_VALIDATORS = [{"NAME":"django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},{"NAME":"django.contrib.auth.password_validation.MinimumLengthValidator"},{"NAME":"django.contrib.auth.password_validation.CommonPasswordValidator"},{"NAME":"django.contrib.auth.password_validation.NumericPasswordValidator"}]
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:5173").split(",")
REST_FRAMEWORK = {"DEFAULT_AUTHENTICATION_CLASSES":["rest_framework_simplejwt.authentication.JWTAuthentication"],"DEFAULT_PERMISSION_CLASSES":["rest_framework.permissions.IsAuthenticated"],"DEFAULT_SCHEMA_CLASS":"drf_spectacular.openapi.AutoSchema"}
SIMPLE_JWT = {"SIGNING_KEY":os.getenv("JWT_SIGNING_KEY", SECRET_KEY),"ACCESS_TOKEN_LIFETIME":__import__('datetime').timedelta(minutes=15),"REFRESH_TOKEN_LIFETIME":__import__('datetime').timedelta(days=1),"ROTATE_REFRESH_TOKENS":True,"BLACKLIST_AFTER_ROTATION":True,"UPDATE_LAST_LOGIN":True}
SPECTACULAR_SETTINGS = {"TITLE":os.getenv("SERVICE_NAME", "Marketplace").title()+" API", "VERSION":"0.1.0", "SERVE_INCLUDE_SCHEMA":False}
INTERNAL_SERVICE_TOKEN = os.getenv("INTERNAL_SERVICE_TOKEN", "unsafe-local-internal-token")

ASGI_APPLICATION = "config.asgi.application"
CHANNEL_LAYERS = {"default":{"BACKEND":"channels_redis.core.RedisChannelLayer","CONFIG":{"hosts":[os.getenv("REDIS_URL","redis://localhost:6379/0")]}}}
