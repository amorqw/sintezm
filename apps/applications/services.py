import logging

import httpx
from django.conf import settings

from .models import TelegramSubscriber

logger = logging.getLogger(__name__)


def notify_telegram(message: str) -> None:
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        logger.info("TELEGRAM_BOT_TOKEN не задан — пропускаем Telegram-уведомление")
        return

    subscribers = TelegramSubscriber.objects.all()
    logger.info(f"Найдено подписчиков: {subscribers.count()}")
    if not subscribers:
        logger.info("Нет подписчиков — пропускаем Telegram-уведомление")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    with httpx.Client(timeout=10.0) as client:
        for subscriber in subscribers:
            try:
                resp = client.post(url, json={"chat_id": subscriber.chat_id, "text": message})
                resp.raise_for_status()
                logger.info(f"Уведомление отправлено подписчику {subscriber.chat_id}")
            except Exception as e:
                logger.exception(f"Ошибка отправки уведомления подписчику {subscriber.chat_id}: {e}")

