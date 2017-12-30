from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3)4uy#y5^)psn09we3_zlc8)=9j3qi7th2lwoqcj@&8c*l1d70'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = [
    '.mlp.com',
]

try:
    from .local import *
except ImportError:
    pass
