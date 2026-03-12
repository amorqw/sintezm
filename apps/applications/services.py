import logging

import httpx
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def notify_manager_email(subject: str, body: str) -> None:
    if not settings.MANAGER_EMAIL:
        logger.info("MANAGER_EMAIL не задан — пропускаем email-уведомление")
        return

    send_mail(
        subject=subject,
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.MANAGER_EMAIL],
        fail_silently=False,
    )


def notify_telegram(message: str) -> None:
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    if not token or not chat_id:
        logger.info("TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID не заданы — пропускаем Telegram-уведомление")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    with httpx.Client(timeout=10.0) as client:
        resp = client.post(url, json={"chat_id": chat_id, "text": message})
        resp.raise_for_status()

