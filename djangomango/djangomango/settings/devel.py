from .base import *  # pylint: disable=W0614,W0401

#==============================================================================
# Generic settings
#==============================================================================

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS += (
    'django_extensions',
    # 'debug_toolbar',
)

#==============================================================================
# Email settings
#==============================================================================

EMAIL_USE_TLS = False

#==============================================================================
# Middleware
#==============================================================================

# MIDDLEWARE_CLASSES += (
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# )

#==============================================================================
# Third party apps settings
#==============================================================================

# django-debug-toolbar
# INTERNAL_IPS = ('127.0.0.1',)
# DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
