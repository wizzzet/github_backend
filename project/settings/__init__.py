import os


def gettext_noop(s):
    return s


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ROOT = os.path.dirname(PROJECT_DIR)

ENV = 'production'
DEBUG = False

ADMINS = (
    ('Rafael Kamashev', 'wizzzet@gmail.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'github',
        'USER': 'github',
        'PASSWORD': 'github',
        'HOST': 'localhost',
        'PORT': '5433'
    }
}

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru'
LANGUAGES = (
    ('ru', gettext_noop('Russian')),
    ('en', gettext_noop('English'))
)
LANGUAGE_CODES = MODELTRANSLATION_LANGUAGES = tuple([x[0] for x in LANGUAGES])
LANGUAGE_CODES_PUBLIC = ('ru', 'en')
DEFAULT_LANGUAGE = MODELTRANSLATION_DEFAULT_LANGUAGE = LANGUAGES[0][0]
MODELTRANSLATION_ENABLE_FALLBACKS = True
MODELTRANSLATION_FALLBACK_LANGUAGES = {
    'default': (),
    'en': ('ru',)
}

MODELTRANSLATION_CUSTOM_FIELDS = ('RichTextUploadingField',)

SITE_ID = 1
SITE_NAME = 'github.wizzzet.ru'
SITE_PROTOCOL = 'https://'
ADMIN_SITE_URL = f'{SITE_PROTOCOL}admin.{SITE_NAME}'

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.normpath(os.path.join(SITE_ROOT, 'public', 'media'))
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.normpath(os.path.join(SITE_ROOT, 'public', 'static'))
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.normpath(os.path.join(SITE_ROOT, 'static')),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

LOCALE_PATHS = (
    os.path.normpath(os.path.join(SITE_ROOT, 'locale')),
)

template_context_processors = (
    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.debug',
    'django.template.context_processors.i18n',
    'django.template.context_processors.media',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.template.context_processors.request'
)
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
        os.path.join(SITE_ROOT, 'templates'),
    ],
    'OPTIONS': {
        'context_processors': template_context_processors,
        'debug': DEBUG,
        'loaders': (
            (
                'django.template.loaders.cached.Loader',
                (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader'
                )
            ),
        )
    }
}]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

MIDDLEWARE = [
    'snippets.middlewares.language.LanguageMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware'
]

ROOT_URLCONF = 'project.urls'

INSTALLED_APPS = (
    'corsheaders',
    'modeltranslation',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'rest_framework',
    'drf_yasg',
    'solo',
    'github'
)

API_APPS = (
    'github',
)

# LOGIN_URL = reverse_lazy('auth_login')
LOGIN_REDIRECT_URL = '/'
LOGIN_ALWAYS_REQUIRED = False
# url, которые игнорируются при проверке входа
LOGIN_EXEMPT_URLS = (r'^media/.*', '^static/.*')

# AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

DATE_FORMAT = 'd.m.Y'
DATETIME_FORMAT = 'd.m.Y H:i:s'
DATE_INPUT_FORMATS = (
    '%Y-%m-%d',
    '%d.%m.%Y',
    '%m/%d/%Y',
    '%m/%d/%y',
    '%b %d %Y',
    '%b %d, %Y',
    '%d %b %Y',
    '%d %b, %Y',
    '%B %d %Y',
    '%B %d, %Y',
    '%d %B %Y',
    '%d %B, %Y'
)
DATETIME_INPUT_FORMATS = (
    '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
    '%Y-%m-%dT%H:%M:%S',
    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
    '%Y-%m-%d',              # '2006-10-25'
    '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
    '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
    '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
    '%m/%d/%Y',              # '10/25/2006'
    '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
    '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
    '%m/%d/%y %H:%M',        # '10/25/06 14:30'
    '%m/%d/%y',              # '10/25/06'
    '%d.%m.%Y %H:%M:%S',
    '%d.%m.%Y %H:%M'
)

DEFAULT_FROM_EMAIL = 'robot@%s' % SITE_NAME
EMAIL_BATCH_SIZE = 100

MPTT_ADMIN_LEVEL_INDENT = 20

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/2',
        'OPTIONS': {
            'DB': 2,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 150,
                'timeout': 20,
            },
            'MAX_CONNECTIONS': 1000,
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        }
    }
}
CACHE_PAGE_TIMEOUT = 60

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'UPLOADED_FILES_USE_URL': False,
    'PAGE_SIZE': 10
}

SWAGGER_SETTINGS = {
    'DEFAULT_INFO': 'project.urls.api_info',
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

GITHUB_API_URL = 'https://api.github.com'
GITHUB_USERNAME = 'XXXX'
GITHUB_PASSWORD = 'XXXX'

try:
    from project.settings.local_settings import *  # NOQA
except ImportError:
    pass


SITE_URL = SITE_PROTOCOL + SITE_NAME
CSRF_TRUSTED_ORIGINS = [SITE_NAME]

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

CORS_ORIGIN_ALLOW_ALL = DEBUG
