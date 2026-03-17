from .base import *  # noqa: F403

DEBUG = False

# Allow Vercel domains and any custom domains you add in env
ALLOWED_HOSTS = [".vercel.app", "sintezm.ru", "www.sintezm.ru", "localhost", "127.0.0.1"]

# Static files for Vercel
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Security defaults (can be overridden via env vars if needed)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = ["https://*.vercel.app", "https://sintezm.ru", "https://www.sintezm.ru"]
