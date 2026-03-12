from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView

from .models import Category, Product


class CatalogIndexView(TemplateView):
    template_name = "catalog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class CategoryView(ListView):
    template_name = "catalog/category.html"
    context_object_name = "products"

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, slug=kwargs["category_slug"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Product.objects.filter(category=self.category, is_active=True).select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class ProductView(DetailView):
    template_name = "catalog/product.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "product_slug"

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related("category")

