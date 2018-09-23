"""
Django settings for qsite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

#----------------------------------------------------------------------
# MAIN
#----------------------------------------------------------------------

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'czc@@6l995r33kpmjeu9%+46yvl0f7!g6$)*3i69+opv^3k3t^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['sdd.pythonanywhere.com', 'www.quotry.com']

ROOT_URLCONF = 'qsite.urls'

WSGI_APPLICATION = 'qsite.wsgi.application'


#----------------------------------------------------------------------
# Auth & Registration
# - auth (django built-in functionality)
# - reg  (django-registration-redux app)
#----------------------------------------------------------------------

# If True, users can register
REGISTRATION_OPEN = False

# One-week activation window; you may, of course, use a different value.
ACCOUNT_ACTIVATION_DAYS = 7

# If True, the user will be automatically logged in.
REGISTRATION_AUTO_LOGIN = True

# Pages requiring authentication redirected not-logined users here
# via login_required() decorator on view functions/methods
LOGIN_URL = '/accounts/login/'

# The page you want users to arrive at after their (!)successful log in
LOGIN_REDIRECT_URL = '/'


#----------------------------------------------------------------------
# Cookies
#----------------------------------------------------------------------

SESSION_COOKIE_AGE = 1209600


#----------------------------------------------------------------------
# Templates
#----------------------------------------------------------------------

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, 'templates'),
]

#----------------------------------------------------------------------
# Static files
# (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
#----------------------------------------------------------------------

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static'),
)

#----------------------------------------------------------------------
# Media
# (uploads)
#----------------------------------------------------------------------

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#----------------------------------------------------------------------
# Applications and Middleware
#----------------------------------------------------------------------

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    #'django.contrib.sites',
    'django.contrib.contenttypes',

    # store session information in a Django model/database
    # model django.contrib.sessions.models.Session
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # my app
    'quotry',

    # django-registration
    'registration',
)

MIDDLEWARE_CLASSES = (
    # enables the creation of unique sessionid cookies
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    # for forms protection (against MitM?)
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

#----------------------------------------------------------------------
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
#----------------------------------------------------------------------

DATABASE_PATH = os.path.join(BASE_DIR, 'quotry.sqlite3')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_PATH,
    }
}

#----------------------------------------------------------------------
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
#----------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

<<<<<<< HEAD

=======
>>>>>>> 8bec420eebcc345376e0bd8effcd26dfa5d016fc
##################
# LOCAL SETTINGS #
##################

try:
    from local_settings import *
except ImportError as e:
    if "local_settings" not in str(e):
        raise e


####################
# DYNAMIC SETTINGS #
####################

try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())