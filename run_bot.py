#!/usr/bin/env python
import os
import sys
import logging

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import django
django.setup()

from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import telegram.error

from apps.applications.models import TelegramSubscriber

logger = logging.getLogger(__name__)


@sync_to_async
def create_or_get_subscriber(chat_id, username, first_name):
    subscriber, created = TelegramSubscriber.objects.get_or_create(
        chat_id=chat_id,
        defaults={
            "username": username,
            "first_name": first_name,
        }
    )
    return subscriber, created


@sync_to_async
def delete_subscriber(chat_id):
    try:
        subscriber = TelegramSubscriber.objects.get(chat_id=chat_id)
        subscriber.delete()
        return True
    except TelegramSubscriber.DoesNotExist:
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = str(update.effective_chat.id)
    username = update.effective_user.username or ""
    first_name = update.effective_user.first_name or ""

    print(f"Попытка подписки: chat_id={chat_id}, username={username}")

    subscriber, created = await create_or_get_subscriber(chat_id, username, first_name)

    if created:
        print(f"Создан новый подписчик: {subscriber}")
        await update.message.reply_text(
            "Вы успешно подписались на уведомления о новых заявках!\n"
            "Используйте /stop для отписки."
        )
    else:
        print(f"Подписчик уже существует: {subscriber}")
        await update.message.reply_text(
            "Вы уже подписаны на уведомления.\n"
            "Используйте /stop для отписки."
        )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = str(update.effective_chat.id)

    deleted = await delete_subscriber(chat_id)

    if deleted:
        print(f"Удалён подписчик: {chat_id}")
        await update.message.reply_text(
            "Вы отписались от уведомлений о заявках.\n"
            "Используйте /start для повторной подписки."
        )
    else:
        await update.message.reply_text(
            "Вы не были подписаны на уведомления.\n"
            "Используйте /start для подписки."
        )


def main():
    from django.conf import settings

    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        print("TELEGRAM_BOT_TOKEN не задан в настройках")
        return

    application = Application.builder().token(token).build()

    # Добавляем обработчик ошибок
    async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        print(f'Update {update} caused error {context.error}')
        # Не логируем Conflict ошибки, чтобы не засорять логи
        if not isinstance(context.error, telegram.error.Conflict):
            logger.error(f'Update {update} caused error {context.error}')

    application.add_error_handler(error_handler)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))

    print("Бот запущен. Нажмите Ctrl+C для остановки.")

    # Запуск бота
    application.run_polling()


if __name__ == "__main__":
    main()