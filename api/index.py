import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

# Initialize Django
application = get_wsgi_application()

# Vercel expects the app to be named 'app'
app = application