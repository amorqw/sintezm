from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.catalog.models import Category, Product
from apps.services.models import Service


class CoreStaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return ["core:index", "core:about", "core:contacts"]

    def location(self, item):
        return reverse(item)


class ServicesSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Service.objects.filter(is_active=True)


class CatalogSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return list(Category.objects.all()) + list(Product.objects.filter(is_active=True))

