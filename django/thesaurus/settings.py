"""
Django settings for thesaurus project.

Generated by 'django-admin startproject' using Django 3.0.5.
"""
import os
import re
from logging.config import dictConfig

from django.core.validators import MinValueValidator
from django.db import DEFAULT_DB_ALIAS
from django.urls import reverse_lazy
from django.utils.log import DEFAULT_LOGGING
from django.utils.translation import gettext_lazy as _

from .config import AutoConfig

config = AutoConfig(search_path='/run/secrets/')  # .env file is injected by docker secrets

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", cast=bool, default=False)

ENVIRONMENT_NAME = config("ENVIRONMENT_LABEL", cast=str, default="Unknown environment")
ENVIRONMENT_COLOR = config("ENVIRONMENT_COLOR", cast=str, default="#777")

VERSION = config('THESAURUS_VERSION', default='unknown')

ALLOWED_HOSTS = config("ALLOWED_HOSTS").split(" ")

INSTALLED_APPS = [
    'django_admin_env_notice',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.postgres',
    'constance',
    'constance.backends.database',

    'apps.audit',

    'apps.accounts',
    'apps.api',
    'apps.attachment',
    'apps.emails',
    'apps.frontend',
    'apps.thesis',
    'apps.review',
    'apps.utils',

    'debug_toolbar',
    'django_better_admin_arrayfield',
    'django_bleach',
    'django_extensions',
    'django_filters',
    'django_python3_ldap',
    'loginas',
    'mailqueue',
    'rest_framework',
    'webpack_loader',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'apps.utils.middleware.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'apps.audit.middleware.AuditMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_USER_MODEL = 'accounts.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django_admin_env_notice.context_processors.from_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'thesaurus.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    DEFAULT_DB_ALIAS: {
        "ENGINE": config("SQL_ENGINE", default="django.db.backends.sqlite3"),
        "NAME": config("SQL_DATABASE", default=os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": config("SQL_USER", default="user"),
        "PASSWORD": config("SQL_PASSWORD", default="password"),
        "HOST": config("SQL_HOST", default="localhost"),
        "PORT": config("SQL_PORT", default="5432"),
        "ATOMIC_REQUESTS": True,
        'OPTIONS': {
            'options': '-c search_path=public,audit'
        },
    }
}

AUDIT_REWRITE_PKS_TO_LABELS_FOR_MODELS = (
    'attachment.TypeAttachment',
    'thesis.Category',
)

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTHENTICATION_BACKENDS = [
    'django_python3_ldap.auth.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGES = (
    ('cs', _('Czech')),
)

LANGUAGE_CODE = 'cs'

TIME_ZONE = config('TZ')

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': False,
        'BUNDLE_DIR_NAME': './',  # must end with slash
        'STATS_FILE': config('BUILD_DIR', default='') + 'webpack-stats.json',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'apps.api.utils.filters.UnAccentSearchFilter',
        'apps.api.utils.filters.RelatedOrderingFilter',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'apps.api.permissions.RestrictedViewModelPermissions',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.api.authentication.SessionAuthentication',
    ),
    'EXCEPTION_HANDLER': 'apps.api.utils.exceptions.exception_handler',
    'PAGE_SIZE': 20,
}

CAN_LOGIN_AS = lambda request, target_user: request.user.is_superuser and not target_user.is_superuser

if DEBUG:
    # for django-debug-toolbar
    # remote_addr does not matter in debug mode in image
    INTERNAL_IPS = type(str('ContainsEverything'), (), {'__contains__': lambda *a: True})()

###### LDAP
# https://github.com/etianen/django-python3-ldap

LDAP_AUTH_URL = f"ldap://{config('LDAP_HOST', cast=str)}:{config('LDAP_PORT', cast=str)}"
LDAP_AUTH_USE_TLS = False
LDAP_AUTH_CONNECTION_USERNAME = config('LDAP_USERNAME', cast=str)
LDAP_AUTH_CONNECTION_PASSWORD = config('LDAP_PASSWORD', cast=str)
LDAP_AUTH_CONNECT_TIMEOUT = None
LDAP_AUTH_RECEIVE_TIMEOUT = None

LDAP_AUTH_SEARCH_BASE = config('LDAP_SEARCH_BASE', cast=str)
LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = config('LDAP_ACTIVE_DIRECTORY_DOMAIN', cast=str)
LDAP_AUTH_OBJECT_CLASS = "organizationalPerson"

LDAP_AUTH_USER_FIELDS = dict(
    username="sAMAccountName",
    first_name="givenName",
    last_name="sn",
    email="userPrincipalName",
)

LDAP_AUTH_USER_LOOKUP_FIELDS = ("username",)

LDAP_AUTH_CLEAN_USER_DATA = "django_python3_ldap.utils.clean_user_data"
LDAP_AUTH_SYNC_USER_RELATIONS = "apps.accounts.ldap.sync_user_relations"
LDAP_AUTH_FORMAT_SEARCH_FILTERS = "django_python3_ldap.utils.format_search_filters"
LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_active_directory_principal"

# custom app config
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'MAX_OPEN_RESERVATIONS_COUNT': (
        6,
        _('Maximal count of opened reservations linked to one user (inclusive).'),
        'non_negative_small_integer',
    ),
}
CONSTANCE_ADDITIONAL_FIELDS = {
    'non_negative_small_integer': ['django.forms.fields.IntegerField', {
        'validators': [
            MinValueValidator(limit_value=0)
        ]
    }],
}
CONSTANCE_SUPERUSER_ONLY = False

# emailing
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
MAILQUEUE_QUEUE_UP: bool = config('EMAIL_USE_QUEUE', default=not DEBUG, cast=bool)
MAILQUEUE_STORAGE = True

DEFAULT_FROM_EMAIL: str = config('MAIL_FROM_ADDRESS', default='noreply@thesaurus')
MAIL_SUBJECT_TITLE: str = config('MAIL_SUBJECT_TITLE', default='Thesaurus')
EMAIL_LANGUAGE = 'cs'

# urls definitions
STATIC_URL = '/static/'

STATIC_ROOT = '/usr/src/static'

# public URL for building absolute urls
PUBLIC_HOST: str = config('PUBLIC_HOST', cast=str)

MEDIA_ROOT = '/usr/src/media'

MEDIA_URL = '/media/'

ROOT_URLCONF = 'thesaurus.urls'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if not DEBUG:
    SECURE_HSTS_SECONDS = 15768000

    SECURE_HSTS_PRELOAD = True

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_REFERRER_POLICY = 'strict-origin'

LOGIN_REDIRECT_URL = reverse_lazy('app')

LOGOUT_REDIRECT_URL = LOGINAS_LOGOUT_REDIRECT_URL = reverse_lazy('login')

LOGIN_URL = reverse_lazy('login')

APPEND_SLASH = False

API_URL_PATTERN = re.compile(r'^/api/.*')

LOCALE_MIDDLEWARE_IGNORE_URLS = (
    API_URL_PATTERN,
)

# logging & sentry
SENTRY_DSN = config('SENTRY_DSN', default='')
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(transaction_style='function_name')],

        send_default_pii=True,
    )

LOGGING_CONFIG = None

LOGLEVEL = config('LOGLEVEL', default='info').upper()

dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
    },
    'loggers': {
        '': {
            'level': 'WARNING',
            'handlers': ['console'],
        },
        'apps': {
            'level': LOGLEVEL,
            'handlers': ['console'],
            'propagate': False,
        },
        'django.server': DEFAULT_LOGGING['loggers']['django.server'],
    },
})
