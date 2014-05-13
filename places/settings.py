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

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

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
    # http://django-mptt.github.io/django-mptt/
    'mptt',
    # https://github.com/thoas/django-discussions
    # disabled because of problems with south migrations.
    #'discussions',
    # http://www.django-rest-framework.org
    'rest_framework',
    # https://github.com/skorokithakis/django-annoying
    'annoying',
    #'python-social-auth',
    'social.apps.django_app.default',
    # django-activity-stream
    'actstream',
    #http://django-taggit.readthedocs.org/en/latest/
    'taggit',
    # Core program modules
    'places_core', # for common templates and static files
    'userspace',
    'locations',
    'ideas',
    'blog',
    'polls',
    'rest',     # out for django rest framework
    'topics',   # custom forum app
    'comments', # custom comments app (using mptt)
    # Database migrations
    'south',
)

# Authentication and python-social-auth settings
AUTHENTICATION_BACKENDS = (
    'social.backends.open_id.OpenIdAuth',
    'social.backends.google.GoogleOpenId',
    'social.backends.google.GoogleOAuth2',
    'social.backends.google.GoogleOAuth',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.yahoo.YahooOpenId',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = '/user/login/'
LOGIN_REDIRECT_URL = '/activity/'
LOGOUT_URL = '/user/logout/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/user/passet/'

# django-activity-stream settings
ACTSTREAM_SETTINGS = {
    'MODELS': ('auth.user', 'auth.group', 'locations.location', 'ideas.idea', 'blog.news'),
    'MANAGER': 'actstream.managers.ActionManager',
    'FETCH_RELATIONS': True,
    'USE_PREFETCH': True,
    'USE_JSONFIELD': True,
    'GFK_FETCH_DEPTH': 1,
}

# django rest framework
REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

TEMPLATE_CONTEXT_PROCESSORS = (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'places.urls'

WSGI_APPLICATION = 'places.wsgi.application'

# Django messages framework
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    50: 'danger',
}

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL   = '/static/'
MEDIA_ROOT   = os.path.join(BASE_DIR, 'media')
MEDIA_URL    = '/media/'


# South database migrations schemes
# http://south.readthedocs.org/en/latest/convertinganapp.html#converting-an-app
SOUTH_MIGRATION_MODULES = {
    'taggit': 'taggit.south_migrations',
}
