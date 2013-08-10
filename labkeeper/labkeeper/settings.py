from django.utils.datastructures import SortedDict

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Jeremy Stretch', 'stretch@packetlife.net'),
)

MANAGERS = ADMINS

# Database configured via local_settings.py
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': '',                      # Or path to database file if using sqlite3.
#         # The following settings are not used with sqlite3:
#         'USER': '',
#         'PASSWORD': '',
#         'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
#         'PORT': '',                      # Set to empty string for default.
#     }
# }

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['labkeeper.net']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

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
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = '/srv/www/labkeeper.net/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/srv/www/labkeeper.net/static_collected/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/s/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/srv/www/labkeeper.net/static/',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request', # Non-default
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'labkeeper.middleware.TimezoneMiddleware',
    'users.middleware.UserTracking',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'labkeeper.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'labkeeper.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/srv/www/labkeeper.net/labkeeper/templates/',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'south',
    'easy_maps',
    'django_tables2',
    'debug_toolbar',

    # Forms stuff
    'django_forms_bootstrap',
    'widget_tweaks',

    # User-generated content
    'django_bleach',
    'tinymce',

    # Local
    'labs',
    'scheduler',
    'radiusd',
    'users',
)

# django-registration
REGISTRATION_OPEN = True
ACCOUNT_ACTIVATION_DAYS = 7

# Bleach
BLEACH_ALLOWED_TAGS = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'i', 'li', 'ol',
                       'p', 'pre', 'strong', 'sub', 'sup', 'ul']
BLEACH_ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'acronym': ['title'],
    'abbr': ['title'],
}
BLEACH_ALLOWED_STYLES = ['padding-left', 'text-align', 'text-decoration']
BLEACH_STRIP_TAGS = True
BLEACH_STRIP_COMMENTS = True
BLEACH_DEFAULT_WIDGET = 'tinymce.widgets.TinyMCE'

# TinyMCE
TINYMCE_JS_URL = 'http://tinymce.cachefly.net/4.0/tinymce.min.js'
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "code,link,paste,table,searchreplace",
    #'theme': "simple",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    'removed_menuitems': 'newdocument',
}

SUPPORTED_TIMEZONES = SortedDict((
    ('Pacific/Midway', 'Midway Island'),
    ('US/Samoa', 'Samoa'),
    ('US/Hawaii', 'Hawaii'),
    ('US/Alaska', 'Alaska'),
    ('US/Pacific', 'Pacific Time (US & Canada)'),
    ('America/Tijuana', 'Tijuana'),
    ('US/Arizona', 'Arizona'),
    ('US/Mountain', 'Mountain Time (US & Canada)'),
    ('America/Chihuahua', 'Chihuahua'),
    ('America/Mazatlan', 'Mazatlan'),
    ('America/Mexico_City', 'Mexico City'),
    ('America/Monterrey', 'Monterrey'),
    ('Canada/Saskatchewan', 'Saskatchewan'),
    ('US/Central', 'Central Time (US & Canada)'),
    ('US/Eastern', 'Eastern Time (US & Canada)'),
    ('US/East-Indiana', 'Indiana (East)'),
    ('America/Bogota', 'Bogota'),
    ('America/Lima', 'Lima'),
    ('America/Caracas', 'Caracas'),
    ('Canada/Atlantic', 'Atlantic Time (Canada)'),
    ('America/La_Paz', 'La Paz'),
    ('America/Santiago', 'Santiago'),
    ('Canada/Newfoundland', 'Newfoundland'),
    ('America/Buenos_Aires', 'Buenos Aires'),
    ('America/Godthab', 'Greenland'),
    ('Atlantic/Stanley', 'Stanley'),
    ('Atlantic/Azores', 'Azores'),
    ('UTC', 'UTC'),
    ('Atlantic/Cape_Verde', 'Cape Verde Is.'),
    ('Africa/Casablanca', 'Casablanca'),
    ('Europe/Dublin', 'Dublin'),
    ('Europe/Lisbon', 'Lisbon'),
    ('Europe/London', 'London'),
    ('Africa/Monrovia', 'Monrovia'),
    ('Europe/Amsterdam', 'Amsterdam'),
    ('Europe/Belgrade', 'Belgrade'),
    ('Europe/Berlin', 'Berlin'),
    ('Europe/Bratislava', 'Bratislava'),
    ('Europe/Brussels', 'Brussels'),
    ('Europe/Budapest', 'Budapest'),
    ('Europe/Copenhagen', 'Copenhagen'),
    ('Europe/Ljubljana', 'Ljubljana'),
    ('Europe/Madrid', 'Madrid'),
    ('Europe/Paris', 'Paris'),
    ('Europe/Prague', 'Prague'),
    ('Europe/Rome', 'Rome'),
    ('Europe/Sarajevo', 'Sarajevo'),
    ('Europe/Skopje', 'Skopje'),
    ('Europe/Stockholm', 'Stockholm'),
    ('Europe/Vienna', 'Vienna'),
    ('Europe/Warsaw', 'Warsaw'),
    ('Europe/Zagreb', 'Zagreb'),
    ('Europe/Athens', 'Athens'),
    ('Europe/Bucharest', 'Bucharest'),
    ('Africa/Cairo', 'Cairo'),
    ('Africa/Harare', 'Harare'),
    ('Europe/Helsinki', 'Helsinki'),
    ('Europe/Istanbul', 'Istanbul'),
    ('Asia/Jerusalem', 'Jerusalem'),
    ('Europe/Kiev', 'Kyiv'),
    ('Europe/Minsk', 'Minsk'),
    ('Europe/Riga', 'Riga'),
    ('Europe/Sofia', 'Sofia'),
    ('Europe/Tallinn', 'Tallinn'),
    ('Europe/Vilnius', 'Vilnius'),
    ('Asia/Baghdad', 'Baghdad'),
    ('Asia/Kuwait', 'Kuwait'),
    ('Africa/Nairobi', 'Nairobi'),
    ('Asia/Riyadh', 'Riyadh'),
    ('Asia/Tehran', 'Tehran'),
    ('Europe/Moscow', 'Moscow'),
    ('Asia/Baku', 'Baku'),
    ('Europe/Volgograd', 'Volgograd'),
    ('Asia/Muscat', 'Muscat'),
    ('Asia/Tbilisi', 'Tbilisi'),
    ('Asia/Yerevan', 'Yerevan'),
    ('Asia/Kabul', 'Kabul'),
    ('Asia/Karachi', 'Karachi'),
    ('Asia/Tashkent', 'Tashkent'),
    ('Asia/Kolkata', 'Kolkata'),
    ('Asia/Yekaterinburg', 'Ekaterinburg'),
    ('Asia/Almaty', 'Almaty'),
    ('Asia/Dhaka', 'Dhaka'),
    ('Asia/Novosibirsk', 'Novosibirsk'),
    ('Asia/Bangkok', 'Bangkok'),
    ('Asia/Jakarta', 'Jakarta'),
    ('Asia/Krasnoyarsk', 'Krasnoyarsk'),
    ('Asia/Chongqing', 'Chongqing'),
    ('Asia/Hong_Kong', 'Hong Kong'),
    ('Asia/Kuala_Lumpur', 'Kuala Lumpur'),
    ('Australia/Perth', 'Perth'),
    ('Asia/Singapore', 'Singapore'),
    ('Asia/Taipei', 'Taipei'),
    ('Asia/Ulaanbaatar', 'Ulaan Bataar'),
    ('Asia/Urumqi', 'Urumqi'),
    ('Asia/Irkutsk', 'Irkutsk'),
    ('Asia/Seoul', 'Seoul'),
    ('Asia/Tokyo', 'Tokyo'),
    ('Australia/Adelaide', 'Adelaide'),
    ('Australia/Darwin', 'Darwin'),
    ('Asia/Yakutsk', 'Yakutsk'),
    ('Australia/Brisbane', 'Brisbane'),
    ('Australia/Canberra', 'Canberra'),
    ('Pacific/Guam', 'Guam'),
    ('Australia/Hobart', 'Hobart'),
    ('Australia/Melbourne', 'Melbourne'),
    ('Pacific/Port_Moresby', 'Port Moresby'),
    ('Australia/Sydney', 'Sydney'),
    ('Asia/Vladivostok', 'Vladivostok'),
    ('Asia/Magadan', 'Magadan'),
    ('Pacific/Auckland', 'Auckland'),
    ('Pacific/Fiji', 'Fiji'),
))

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
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
    }
}

# Import local settings
try:
    from local_settings import *
except:
    pass

