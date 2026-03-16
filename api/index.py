import os
from django.core.wsgi import get_wsgi_application
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

# Initialize Django
application = get_wsgi_application()

# Vercel serverless function handler
def handler(event, context):
    # This is a basic handler for Vercel
    # Vercel will handle the WSGI application automatically
    return application