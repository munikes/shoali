# Django settings for shoali project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)

ADMINS = (
     ('mUniKeS', 'munikes@members.fsf.org'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'shoali',          # Or path to database file if using sqlite3.
        'USER': 'shoali',          # Not used with sqlite3.
        'PASSWORD': 'shoali321',   # Not used with sqlite3.
        'HOST': 'localhost',       # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-ES'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'rvop$va(p1lr0h3e@uoi-pgqy2ze_g977e7%b&amp;+5pta@7s%8@i'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'main.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'main.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #os.path.join(BASE_DIR, "template")
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'main.apps.core',
    'django_extensions',
    'djcelery',
    'registration',
    'captcha',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
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
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/shoali/error.log',
            'formatter': 'verbose'
        },
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/shoali/debug.log',
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'main.apps.core': {
            'handlers': ['console', 'file_error', 'file_debug'],
            'level': 'DEBUG',
        }
    }
}

LOGIN_REDIRECT_URL = '/user/'
# This is the number of days users will have to activate their accounts after$
# registering. If a user does not activate within that period, the account will
# remain permanently inactive and may be deleted by maintenance scripts
# provided in django-registration.
ACCOUNT_ACTIVATION_DAYS = 7

# Storing additional information about users
AUTH_PROFILE_MODULE = 'core.ShoaliUser'

# Captcha - google.com/recaptcha
RECAPTCHA_PUBLIC_KEY = '6LePlukSAAAAAG79GF150tQATBb5LKzYqlQL4VRH'
RECAPTCHA_PRIVATE_KEY = '6LePlukSAAAAAKCT9IjIzMGr60hQx3eJisBkfORE'
RECAPTCHA_USE_SSL = True
RECAPTCHA_TESTING = True

# SMTP mail server
EMAIL_HOST='mail.shoali.org'
EMAIL_PORT=25
EMAIL_HOST_USER='admin@shoali.org'
EMAIL_HOST_PASSWORD='shoali321'
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL = 'non-reply@shoali.org'

# Celery config
import djcelery
djcelery.setup_loader()
BROKER_URL = 'mongodb://localhost/celery'

CELERY_RESULT_BACKEND = 'mongodb'
CELERY_MONGODB_BACKEND_SETTINGS = {
    'host': BROKER_URL,
    'taskmeta_collection': 'shoali_taskmeta' # Collection name to use for task output
}
#BROKER_BACKEND = 'mongodb'
#BROKER_HOST = 'localhost'
#BROKER_PORT = 27017
#BROKER_USER = ''
#BROKER_PASSWORD = ''
#BROKER_VHOST = 'celery'

# Find and register all celery tasks.  Your tasks need to be in a
# tasks.py file to be picked up.
CELERY_IMPORTS = ('main.apps.core.tasks', )
