"""
Django settings for vestblog project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import socket

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# sys.path.append(os.path.join('..', 'vest', BASE_DIR))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*t!#gk4uqkf!8-&5ceo%l-o5g)v-1j%kl61fpve+o)lp&v3mw+'

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ['vestlite.ru', 'www.vestlite.ru']


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # vendor
    'grappelli.dashboard',
    'grappelli',
    'django.contrib.admin',
    'filebrowser',
    'django_jinja',
    'django_ace',

    # project
    'common',
    'frontend',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'vestblog.middleware.MiddlewareLocale',
    'vestblog.middleware.MiddlewareSessionExist',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'vestblog.middleware.MiddlewareSimplePage',
    # 'vestblog.middleware.MiddlewareCategory',

)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'vestblog.context_processors.site_info'
)

ROOT_URLCONF = 'vestblog.urls'

WSGI_APPLICATION = 'vestblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
#
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = u'ru'

LANGUAGES = (
    (u'ru', u'Russian'),
    (u'en', u'English'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_remote')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_LOADERS = (
    'common.loaders.load_template_source',

    'django_jinja.loaders.FileSystemLoader',
    'django_jinja.loaders.AppLoader',

    # 'django.template.loaders.filesystem.Loader',
    # 'django.template.loaders.app_directories.Loader',

    # 'django.template.loaders.eggs.Loader',
)

DEFAULT_JINJA2_TEMPLATE_EXTENSION = '.j2'
DEFAULT_TEMPLATE_EXT = '.j2'

GRAPPELLI_INDEX_DASHBOARD = {
    'vestblog.admin_super.admin_super': 'vestblog.dashboard_super.CustomIndexDashboard',
    # 'vestblog.admin_client.admin_client': 'vestblog.dashboard_client.CustomIndexDashboard',

}

HOSTS = ['ld1', 'ld2', 'ld-mac.loc', '192']
LOCAL = False

JINJA2_ENVIRONMENT_OPTIONS = {
    'trim_blocks': True,
    'autoescape': False,
    'cache_size': 0  # TODO: set cache only for static
}

SITE_INFO = {
    'SITESUBTITLE': 'My blog'
}

SITE_ID = 1

if not socket.gethostname() in HOSTS:

    from settings_remote import *
else:
    from settings_local import *
