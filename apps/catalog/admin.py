from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "order", "slug"]
    list_editable = ["order"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["order", "name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "is_active", "price_display", "is_price_on_request", "created_at"]
    list_filter = ["is_active", "category", "created_at"]
    list_editable = ["is_active"]
    search_fields = ["name", "slug", "article_number"]
    prepopulated_fields = {"slug": ("name",)}
    raw_id_fields = ["category"]

