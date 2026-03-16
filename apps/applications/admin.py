from django.contrib import admin

from .models import Application, TelegramSubscriber


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["created_at", "name", "phone", "source", "status", "service", "product"]
    list_filter = ["status", "source", "created_at"]
    list_editable = ["status"]
    search_fields = ["name", "phone", "email"]
    readonly_fields = ["name", "phone", "email", "message", "service", "product", "source", "created_at"]
    date_hierarchy = "created_at"


@admin.register(TelegramSubscriber)
class TelegramSubscriberAdmin(admin.ModelAdmin):
    list_display = ["chat_id", "username", "first_name", "subscribed_at"]
    search_fields = ["chat_id", "username", "first_name"]
    readonly_fields = ["chat_id", "username", "first_name", "subscribed_at"]

