from django.conf import settings


def site_defaults(request):
    return {
        "SITE_NAME": "Синтез М",
        "SITE_DOMAIN": (settings.ALLOWED_HOSTS[0] if getattr(settings, "ALLOWED_HOSTS", None) else "sintez-m.ru"),
    }

