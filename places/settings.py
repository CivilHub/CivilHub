# -*- coding: utf-8 -*-
from __future__ import absolute_import
import djcelery
djcelery.setup_loader()
"""
Django settings for places project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c1ahg2n8_qtu36pg+qp7f92&bugk6k2mpm=qh#y@jtzi-(^rl-'

#~ RECAPTCHA_PUBLIC_KEY = '6LdNLPQSAAAAAIUZQ14Atth5VBL45JwN-8_G0BiU'
#~ RECAPTCHA_PRIVATE_KEY = '98dfg6df7g56df6gdfgdfg65JHJH656565GFGFGs'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']

SITE_ID = 1

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    #http://docs.celeryproject.org/en/latest/getting-started/brokers/django.html#broker-django
    'kombu.transport.django',
    'djcelery',
    # http://niwibe.github.io/djmail/
    'djmail',
    # https://django-modeltranslation.readthedocs.org/en/latest/
    'modeltranslation',
    # http://django-haystack.readthedocs.org/en/latest/
    'haystack',
    # https://github.com/praekelt/django-recaptcha
    #'captcha',
    # https://github.com/SmileyChris/easy-thumbnails
    'easy_thumbnails',
    # http://django-mptt.github.io/django-mptt/
    'mptt',
    # https://github.com/thoas/django-discussions
    # disabled because of problems with south migrations.
    #'discussions',
    # http://www.django-rest-framework.org
    'rest_framework',
    'rest_framework.authtoken',
    # https://github.com/ottoyiu/django-cors-headers
    'corsheaders',
    # https://github.com/skorokithakis/django-annoying
    'annoying',
    #'python-social-auth',
    'social.apps.django_app.default',
    # django-activity-stream
    'actstream',
    #http://django-taggit.readthedocs.org/en/latest/
    'taggit',
    # geodjango
    'django.contrib.gis',
    # Core program modules
    'places_core', # for common templates and static files
    'geobase',  # Kraje, języki i wszystko, co powiązane z mapą
    'userspace',# panel użytkownika
    'locations',
    'ideas',     
    'blog',
    'polls',
    'rest',     # out for django rest framework
    'topics',   # custom forum app
    'comments', # custom comments app (using mptt)
    'gallery',  # user media app
    'south',    # Database migrations
    'maps',     # Custom app for Google Maps
    'staticpages', # Statyczne strony
    'civmail',  # Newsletter i obsługa maili
    'articles', # Statyczne artykuły - support etc.
    #'import_export',
    'raven.contrib.django.raven_compat',
    'analytical',
)


# Core django settings
#-------------------------------------------------------------------------------
TEMPLATE_CONTEXT_PROCESSORS = (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
)
TEMPLATE_DIRS = os.path.join(BASE_DIR, 'templates')


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'places_core.middleware.SubdomainMiddleware',
    # odkomentować na produkcji - wyświetlanie błędów w social_auth
    #'places_core.middleware.SocialAuthExceptionMiddleware',
)

ROOT_URLCONF = 'places.urls'

WSGI_APPLICATION = 'places.wsgi.application'

SESSION_COOKIE_DOMAIN = '.civilhub.org'

# Django messages framework
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    50: 'danger',
}

POSTGIS_VERSION = (2,1,3)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'expose',                      
        'USER': 'expose',
        'PASSWORD': 'civilian14!a',
        'HOST': '172.17.0.36',
        'PORT': 5432,
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL   = '/static/'
STATIC_ROOT  = '../static/'
MEDIA_ROOT   = '../media/'
MEDIA_URL    = '/media/'

# Haystack - search engine
#-------------------------------------------------------------------------------
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

# Social Auth
#-------------------------------------------------------------------------------
# Authentication and python-social-auth settings
AUTHENTICATION_BACKENDS = (
    'social.backends.google.GooglePlusAuth',
    #'social.backends.open_id.OpenIdAuth',
    #'social.backends.google.GoogleOpenId',
    #'social.backends.google.GoogleOAuth2',
    #'social.backends.google.GoogleOAuth',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.facebook.FacebookOAuth2',
    #'social.backends.twitter.Facebook2OAuth2',
    #'social.backends.yahoo.YahooOpenId',
    'social.backends.linkedin.LinkedinOAuth',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = '/user/login/'
LOGIN_REDIRECT_URL = '/activity/'
LOGOUT_URL = '/user/logout/'
SOCIAL_AUTH_UID_LENGTH = 255
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/places/'
# Custom setting - dla użytkowników Twittera
SOCIAL_AUTH_SET_TWITTER_EMAIL_URL = '/user/twitter_email/'
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'places_core.social_auth.set_twitter_email',
    'places_core.social_auth.validate_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'places_core.social_auth.create_user_profile',
    'places_core.social_auth.update_user_social_profile',
)

# New Google+ login
SOCIAL_AUTH_GOOGLE_PLUS_KEY = '621695853095-7p2mrjthfvma0rq0loolpoocq6f94577.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_PLUS_SECRET = 'y4xJ9Vr18aQAkhyp8DDkaz5l'
SOCIAL_AUTH_GOOGLE_PLUS_SCOPE = ['https://www.googleapis.com/auth/plus.login',
                                 'https://www.googleapis.com/auth/userinfo.email',
                                 'https://www.googleapis.com/auth/userinfo.profile',
                                 'https://www.googleapis.com/auth/plus.profile.emails.read',
                                 'https://www.googleapis.com/auth/plus.me',
                                 'https://www.google.com/m8/feeds',]

SOCIAL_AUTH_FACEBOOK_KEY = '345109858975991'
SOCIAL_AUTH_FACEBOOK_SECRET = '685c46b205d4aa87deee26826b1ca958'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'public_profile', 'user_friends', 'user_birthday']

SOCIAL_AUTH_TWITTER_KEY = 'OMqEsrvkxHgMuwEs4FZWWkr4q'
SOCIAL_AUTH_TWITTER_SECRET = 'SDlUX3bxzZdjF1quH3VtSDg34XAA8Are8pIU461kVLiRjHn5H8'

SOCIAL_AUTH_LINKEDIN_KEY = '77uveqo8v3tk5v'
SOCIAL_AUTH_LINKEDIN_SECRET = 'PSsrYr0Acg4BdKWM'
SOCIAL_AUTH_LINKEDIN_FIELD_SELECTORS = ['email-address', 'headline',]
SOCIAL_AUTH_LINKEDIN_EXTRA_DATA = [('id', 'id'),
                                   ('firstName', 'first_name'),
                                   ('lastName', 'last_name'),
                                   ('emailAddress', 'email_address'),
                                   ('headline', 'headline'),
                                   ('industry', 'industry')]


# Actstreams
#-------------------------------------------------------------------------------
# django-activity-stream settings
ACTSTREAM_SETTINGS = {
    'MODELS': ('auth.user', 'auth.group', 'locations.location', 'ideas.idea',
               'blog.news', 'polls.poll', 'comments.customcomment',
               'topics.discussion', 'userspace.userprofile', 'userspace.badge',
               'gallery.locationgalleryitem', 'topics.entry', 'articles.article'),
    'MANAGER': 'actstream.managers.ActionManager',
    'FETCH_RELATIONS': True,
    'USE_PREFETCH': True,
    'USE_JSONFIELD': True,
    'GFK_FETCH_DEPTH': 1,
}

# REST framework
#-------------------------------------------------------------------------------
# django rest framework
REST_FRAMEWORK = {
    'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'per_page',
    'MAX_PAGINATE_BY': 100,
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}

# CORS settings
# IMPORTANT - Be sure to change this settings in production
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'accept-encoding',
)

# Internationalization
#-------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGES = (
    ('en', 'English'),
    ('pl', 'Polski'),
    ('es', 'Español'),
    ('de', 'Niemiecki'),
    ('pt', 'Português'),
    ('fr', 'Français'),
    ('it', 'Italiano'),
    ('cz', 'Ceština'),
)


# REDIS CACHE

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379:1',
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
        }
    }
}


# Email settings
#-------------------------------------------------------------------------------
# Email account settings
EMAIL_HOST          = 'mail.civilhub-mail.org'
EMAIL_PORT          = 587
EMAIL_HOST_USER     = 'noreply@civilhub-mail.org'
EMAIL_HOST_PASSWORD = 'JATUnZCBr9WKEJg4w'
EMAIL_USE_TLS       = False
# Enter real email address here in future
EMAIL_DEFAULT_ADDRESS = 'noreply@civilhub-mail.org'
DEFAULT_FROM_EMAIL = 'noreply@civilhub-mail.org'

# Email settings for testing purposes
#EMAIL_BACKEND       = "djmail.backends.default.EmailBackend"
# Uncomment below line to enable sending real emails.
DJMAIL_REAL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


# Celery/Rabbit i taski
#-------------------------------------------------------------------------------
# Celery task manager settings
BROKER_URL               = 'amqp://guest:guest@localhost:5672//'
CELERY_TASK_SERIALIZER   = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT    = ['json']
CELERY_TIMEZONE          = 'Europe/Warsaw'
CELERY_ENABLE_UTC        = True
CELERY_RESULT_BACKEND    = 'djcelery.backends.database:DatabaseBackend'
# Uncomment following line to enable django caching system for Celery. Remember
# to comment out above backend declaration used for development.
#CELERY_RESULT_BACKEND   = 'djcelery.backends.cache:CacheBackend'
CELERY_IMPORTS = ('places_core.tasks',)
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"


# Ustawienia dla miniaturek
#-------------------------------------------------------------------------------
# For each of set of size image thumbnals will be generated automatically.
THUMB_SIZES = [
    (30, 30),
    (128, 128),
    (256, 256),
]
# Maximum size for pictures in gallery. Bigger pictures will be thumbnailed.
IMAGE_MAX_SIZE = (1024,1024)
GALLERY_THUMB_SIZE = (270,170)

# Maximum size for location and profile pages background images
BACKGROUND_IMAGE_SIZE = (1920, 300)

# Settings for user avatar pictures
AVATAR_SIZE = (128, 128)
AVATAR_THUMBNAIL_SIZES = [
    (30, 30),
    (60, 60),
    (90, 90),
    (120, 120),
]


# South database migrations schemes
# ------------------------------------------------------------------------------
# http://south.readthedocs.org/en/latest/convertinganapp.html#converting-an-app
SOUTH_MIGRATION_MODULES = {
    'taggit': 'taggit.south_migrations',
}


# Sanitize input/output
# ------------------------------------------------------------------------------
VALID_TAGS = ['p','i','strong','b','u','a','pre','br','img','hr','ul','ol',]
VALID_ATTRS = ['href','src','width','height','style','target',]
URL_ATTRS = ['href','src',]


# GeoIP settings
#-------------------------------------------------------------------------------
GEOIP_PATH = os.path.join(BASE_DIR, 'geobase', 'data')
GEOIP_COUNTRY = 'GeoIP.dat'
GEOIP_CITY = 'GeoLiteCity.dat'

# Custom module settings
#-------------------------------------------------------------------------------
COUNTRY_STORAGE_PATH = os.path.join(BASE_DIR, 'geobase', 'markers')
DEFAULT_COUNTRY_CODE = 'US'
# Limit paginatora dla widoków list (lista dyskusji, ankiet etc.)
LIST_PAGINATION_LIMIT = 50
# Limit paginatora dla innych widoków (lista pomysłów, blog etc.)
PAGE_PAGINATION_LIMIT = 5
# Limit paginatora dla actstreamu dla usera (w zamierzeniu dla wszystkich)
STREAM_PAGINATOR_LIMIT = 25
# Limit paginatora dla obrazów w galerii użytkownika
USER_GALLERY_LIMIT = 12
# Limit paginatora dla obrazów w galerii lokalizacji
PLACE_GALLERY_LIMIT = 12

# Customowe ustawienia dla redisa, wyłącza cache w widokach dla
# wersji developerskiej.
USE_CACHE = True


RAVEN_CONFIG = {
    'dsn': 'https://bf265529465747a3b571d206b31f8bdd:070be6ed13684671b317e6a9ce053679@app.getsentry.com/29087',
}

SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'

#Analitical
CLICKY_SITE_ID = '100769640'
