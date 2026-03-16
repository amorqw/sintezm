from django.http import HttpResponse
from django.views.generic import TemplateView, View
import os

from apps.catalog.models import Category
from apps.services.models import Service


class HealthCheckView(View):
    def get(self, request):
        return HttpResponse("OK", content_type="text/plain")


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["services"] = Service.objects.filter(is_active=True).order_by("order", "name")[:6]
        context["categories"] = Category.objects.all().order_by("order", "name")[:8]
        return context


class AboutView(TemplateView):
    template_name = "core/about.html"


class ContactsView(TemplateView):
    template_name = "core/contacts.html"


class RobotsTxtView(View):
    def get(self, request, *args, **kwargs):
        content = "\n".join(
            [
                "User-agent: *",
                "Disallow: /admin/",
                "Allow: /",
                "",
                "Sitemap: /sitemap.xml",
                "",
            ]
        )
        return HttpResponse(content, content_type="text/plain; charset=utf-8")

