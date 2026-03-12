from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["created_at", "name", "phone", "source", "status", "service", "product"]
    list_filter = ["status", "source", "created_at"]
    list_editable = ["status"]
    search_fields = ["name", "phone", "email"]
    readonly_fields = ["name", "phone", "email", "message", "service", "product", "source", "created_at"]
    date_hierarchy = "created_at"

