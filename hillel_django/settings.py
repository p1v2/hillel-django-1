"""
Django settings for hillel_django project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
from datetime import timedelta
from pathlib import Path

import dj_database_url
from celery.schedules import crontab
from dotenv import load_dotenv
import os

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY_PATH = os.path.join(BASE_DIR, "secret_key.txt")
SECRET_KEY = open(os.path.join(BASE_DIR, "secret_key.txt")).read() \
    if os.path.exists(SECRET_KEY_PATH) else "SomeDummySecretKey"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG") == "True"

ALLOWED_HOSTS = ["localhost", "hillel-django.herokuapp.com"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'rest_framework',
    'rest_framework.authtoken',
    'django_celery_beat',
    'django_filters',
    'drf_yasg',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'celery',
    'books',
    'customers',
    'django_celery_results',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'hillel_django.middleware.CustomLoggingMiddleware',
    # "django.middleware.cache.UpdateCacheMiddleware",
    # "django.middleware.common.CommonMiddleware",
    # "django.middleware.cache.FetchFromCacheMiddleware",
]

CACHE_MIDDLEWARE_SECONDS = 5

ROOT_URLCONF = 'hillel_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'hillel_django.authentication.SecretHeaderAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'] if not DEBUG else [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}

WSGI_APPLICATION = 'hillel_django.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

USE_POSTGRES = os.environ.get("USE_POSTGRES") == "True"

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    DEFAULT_DATABASE = dj_database_url.parse(DATABASE_URL)
elif USE_POSTGRES:
    DEFAULT_DATABASE = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ["DB_NAME"],
        'USER': os.environ["DB_USERNAME"],
        'PASSWORD': os.environ["DB_PASSWORD"],
        'HOST': os.environ["DB_HOST"],
        'PORT': '5432',
    }
else:
    DEFAULT_DATABASE = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite',
    }

DATABASES = {
    'default': DEFAULT_DATABASE,
    #'student': dj_database_url.parse("postgres://vgzibcntmwkwjt:fa5731545dbdb678b43e21db8ba7e214225d3bc7eec20ebd87f1d2cfce50e636@ec2-34-250-252-161.eu-west-1.compute.amazonaws.com:5432/df6mqa9p7d1v6o")
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / "static"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CELERY_TIMEZONE = "GMT"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

REDIS_HOST = os.environ.get("REDIS_HOST")

# Celery with Redis
# CELERY_BROKER_URL = f"redis://{REDIS_HOST}:6379"
# CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:6379"

# Celery with RabbitMQ
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")
CELERY_BROKER_URL = os.environ.get("CLOUDAMQP_URL", f"amqp://guest:guest@{RABBITMQ_HOST}:5672/")
CELERY_RESULT_BACKEND = 'django-db'


CELERY_BEAT_SCHEDULE = {
    'run_every_5_seconds': {
        'task': 'books.tasks.run_every_5_seconds',
        'schedule': timedelta(seconds=5),
    },
    'run_on_cron_schedule': {
        'task': 'books.tasks.run_on_cron_schedule',
        'schedule': crontab("*", "*", "*", "*", "*"),
    },
    'timetable_sending':{
        'task': 'books.tasks.timetable_sending',
        'schedule': crontab("12", "45", "*", "*", "*")
    }
}

# if DEBUG:
#     EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
#     EMAIL_FILE_PATH = '/tmp/app-messages'
# else:

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ["GMAIL_FROM_EMAIL"]
EMAIL_HOST_PASSWORD = os.environ["GMAIL_KEY"] #past the key or password app here
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ["GMAIL_FROM_EMAIL"]


LOGGING = {
    'version': 1,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
}


# # Redis cache
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": f"redis://{REDIS_HOST}:6379",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }

# In-memory cache
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
#         "LOCATION": "unique-snowflake"
#     }
# }

# File cache
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
#         "LOCATION": "/tmp/django_cache"
#     }
# }

# Memcached cache
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
#         "LOCATION": "",
#     }
# }

# Database cache
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.db.DatabaseCache",
#         "LOCATION": "my_cache_table",
#     }
# }

# Dummy cache
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.dummy.DummyCache",
#     }
# }

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },

}

# Django-allauth
SITE_ID = 2

LOGIN_REDIRECT_URL = '/admin'
LOGOUT_REDIRECT_URL = '/'

SOCIALACCOUNT_STORE_TOKENS = True

GRAPHENE = {
    "SCHEMA": "hillel_django.schema.schema"
}

