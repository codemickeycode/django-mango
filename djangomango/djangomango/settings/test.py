from .base import *  # pylint: disable=W0614,W0401


#==============================================================================
# Generic settings
#==============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'djangomango',
        'USER': ':memory:',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

#==============================================================================
# Installed apps
#==============================================================================

INSTALLED_APPS += (
    'django_nose',
)

#==============================================================================
# Test specific settings
#==============================================================================

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=usernameless',
]
