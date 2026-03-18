import logging
from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View

from apps.catalog.models import Product
from apps.services.models import Service

from .models import Application
from .services import notify_telegram

logger = logging.getLogger(__name__)


def _get_source_display(source: str) -> str:
    return dict(Application.SOURCE_CHOICES).get(source, "Общая")


def _telegram_text(app: Application) -> str:
    # Добавляем 2 часа к времени создания (если нужно смещение)
    created_time = timezone.localtime(app.created_at) + timedelta(hours=2)
    created = created_time.strftime("%d.%m.%Y %H:%M")

    lines = [
        "🔔 Новая заявка с сайта!",
        "",
        f"👤 Имя: {app.name}",
        f"📞 Телефон: {app.phone}",
        f"📧 Email: {app.email or 'не указан'}",
        f"📍 Источник: {_get_source_display(app.source)}",
    ]

    if app.service_id:
        lines.append(f"🛠 Услуга: {app.service.name} (id={app.service_id})")
    if app.product_id:
        lines.append(f"📦 Товар: {app.product.name} (id={app.product_id})")

    lines.append(f"💬 Сообщение: {app.message or 'не указано'}")
    lines.append("")
    lines.append(f"🕒 {created}")

    return "\n".join(lines)


class ApplyView(View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        name = (data.get("name") or "").strip()
        phone = _normalize_phone((data.get("phone") or "").strip())
        email = (data.get("email") or "").strip()
        message = (data.get("message") or "").strip()
        source = (data.get("source") or "general").strip() or "general"

        service_id = (data.get("service_id") or "").strip()
        product_id = (data.get("product_id") or "").strip()

        if not name or not phone or not email:
            return self._fail(request, "Имя, телефон и email обязательны")

        service = None
        product = None
        if service_id.isdigit():
            service = Service.objects.filter(pk=int(service_id), is_active=True).first()
            if service:
                source = "service"
        if product_id.isdigit():
            product = Product.objects.filter(pk=int(product_id), is_active=True).first()
            if product:
                source = "product"

        app = Application.objects.create(
            name=name,
            phone=phone,
            email=email,
            message=message,
            source=source if source in dict(Application.SOURCE_CHOICES) else "general",
            service=service,
            product=product,
        )

        try:
            notify_telegram(_telegram_text(app))
        except Exception:
            logger.exception("Ошибка отправки Telegram по заявке id=%s", app.id)

        if _is_ajax(request):
            return JsonResponse({"success": True})

        next_url = (data.get("next") or request.META.get("HTTP_REFERER") or "/").strip()
        if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
            next_url = "/"
        separator = "&" if "?" in next_url else "?"
        return redirect(f"{next_url}{separator}success=1")

    def _fail(self, request, message: str):
        if _is_ajax(request):
            return JsonResponse({"success": False, "error": message}, status=400)

        next_url = (request.POST.get("next") or request.META.get("HTTP_REFERER") or "/").strip()
        if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
            next_url = "/"
        separator = "&" if "?" in next_url else "?"
        return redirect(f"{next_url}{separator}error=1")


def _is_ajax(request) -> bool:
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def _normalize_phone(raw: str) -> str:
    digits = "".join(ch for ch in raw if ch.isdigit())
    if not digits:
        return ""

    if digits[0] == "8":
        digits = "7" + digits[1:]
    elif digits[0] == "9" and len(digits) == 10:
        digits = "7" + digits

    if digits[0] != "7":
        return raw

    digits = digits[:11]
    if len(digits) < 11:
        return raw

    return "+7" + digits[1:]
