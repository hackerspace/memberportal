import os
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'NAME'   : '%s/db/db.sqlite' % ROOT_PATH,
        'ENGINE' : 'django.db.backends.sqlite3',
    }
}

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_USE_TLS = False
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''
#DEFAULT_FROM_EMAIL = ''

ADMINS = (
     ('root', 'root@localhost'),
)

MANAGERS = ADMINS

DATE_FORMAT = 'j. F Y'
DATETIME_FORMAT = 'j. F Y h:i:s'
TIME_FORMAT = 'h:i:s'
YEAR_MONTH_FORMAT = 'F Y'
MONTH_DAY_FORMAT = 'j. N.'


SITE_ID = 1

TIME_ZONE = 'Europe/Prague'
LANGUAGE_CODE = 'en'
USE_I18N = True
USE_L10N = True
USE_TZ   = False

MEDIA_URL = '/memberportal/media/'
MEDIA_ROOT = os.path.join(ROOT_PATH, 'media')

STATIC_URL = '/memberportal/static/'
STATIC_ROOT = os.path.join(ROOT_PATH, 'static')

STATICFILES_DIRS = ()

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH, 'templates'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = ( 
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
#    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    'django.middleware.gzip.GZipMiddleware',
)

ROOT_URLCONF = 'memberportal.urls'
WSGI_APPLICATION = 'memberportal.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sites',
#    'django.contrib.comments',
#    'django.contrib.sitemaps',

    'django_extensions',
    'bootstrap_toolkit',
    'registration',
    'baseprofile',
    'payments',
    'captcha',
    'south',
)

ACCOUNT_ACTIVATION_DAYS = 1
AUTH_PROFILE_MODULE = 'baseprofile.BaseProfile'
CAPTCHA_NOISE_FUNCTIONS = ()
CAPTCHA_LETTER_ROTATION = None
MEMBER_STATUS_EMAIL_NOTIFY = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
   'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'DEBUG',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

execfile(os.path.join(ROOT_PATH, 'localsettings.py'))
