
from pathlib import Path
from datetime import timedelta
from config import get_config
import string


CONFIG = get_config()
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = CONFIG.django.secret_key


SPECTACULAR_SETTINGS = {
    "TITLE": f"{CONFIG.name} API",
    "DESCRIPTION": f"{CONFIG.name} API documentation",
    "VERSION": CONFIG.version,
    "SERVE_INCLUDE_SCHEMA": False
}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=CONFIG.jwt.access_lifetime),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=CONFIG.jwt.refresh_lifetime),
    "AUTH_HEADER_TYPES": ("Bearer", ),
}
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}


DEBUG = True
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 16
MAX_USERNAME_LENGTH = 16
ALLOWED_USERNAME_CHARS = string.ascii_letters + string.digits + "-_"


ALLOWED_HOSTS = CONFIG.django.allowed_hosts
ROOT_URLCONF = 'Config.urls'
ASGI_APPLICATION = 'Config.asgi.application'
WSGI_APPLICATION = 'Config.wsgi.application'


CELERY_BROKER_URL = f"redis://{CONFIG.redis.host}:{CONFIG.redis.port}/0"
CELERY_RESULT_BACKEND = f"redis://{CONFIG.redis.host}:{CONFIG.redis.port}/0"


AUTH_USER_MODEL = "Users.User"
DATABASES = {
    'default': {
        'ENGINE': CONFIG.database.engine,
        'NAME': CONFIG.database.name,
        'USER': CONFIG.database.user,
        'PASSWORD': CONFIG.database.password,
        'HOST': CONFIG.database.host,
        'PORT': CONFIG.database.port
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 1209600
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_CACHE_ALIAS = "default"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{CONFIG.redis.host}:{CONFIG.redis.port}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

INTERNAL_APPS = [
    'Core',
    'Users',
    'Events'
]
EXTERNAL_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    'whitenoise',
    "rest_framework_simplejwt.token_blacklist",
]
INSTALLED_APPS = INTERNAL_APPS + EXTERNAL_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

LOGGING_CONFIG = None

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': MIN_PASSWORD_LENGTH},
    },
    {
        'NAME': 'Users.validators.PasswordValidator',
    },
]