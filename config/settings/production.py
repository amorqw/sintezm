from .base import *  # noqa: F403

import os

DEBUG = False

# Production settings for Railway and other platforms
# Prefer env ALLOWED_HOSTS from base; fallback to main domain
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["sintezm.ru", "www.sintezm.ru"]
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = ["https://sintezm.ru", "https://www.sintezm.ru"]

# Logging for production (console output)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        }
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'verbose'},
    },
    'root': {'handlers': ['console'], 'level': 'INFO'},
}

