import os
import sys
import logging

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import django
from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from applications.models import TelegramSubscriber

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Запуск Telegram бота для подписки на уведомления о заявках"

    def handle(self, *args, **options):
        from django.conf import settings

        token = settings.TELEGRAM_BOT_TOKEN
        if not token:
            self.stdout.write(
                self.style.ERROR("TELEGRAM_BOT_TOKEN не задан в настройках")
            )
            return

        application = Application.builder().token(token).build()

        # Обработчик команды /start
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            chat_id = str(update.effective_chat.id)
            username = update.effective_user.username or ""
            first_name = update.effective_user.first_name or ""

            self.stdout.write(f"Попытка подписки: chat_id={chat_id}, username={username}")

            subscriber, created = TelegramSubscriber.objects.get_or_create(
                chat_id=chat_id,
                defaults={
                    "username": username,
                    "first_name": first_name,
                }
            )

            if created:
                self.stdout.write(f"Создан новый подписчик: {subscriber}")
                await update.message.reply_text(
                    "Вы успешно подписались на уведомления о новых заявках!\n"
                    "Используйте /stop для отписки."
                )
            else:
                self.stdout.write(f"Подписчик уже существует: {subscriber}")
                await update.message.reply_text(
                    "Вы уже подписаны на уведомления.\n"
                    "Используйте /stop для отписки."
                )

        # Обработчик команды /stop
        async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            chat_id = str(update.effective_chat.id)

            try:
                subscriber = TelegramSubscriber.objects.get(chat_id=chat_id)
                subscriber.delete()
                await update.message.reply_text(
                    "Вы отписались от уведомлений о заявках.\n"
                    "Используйте /start для повторной подписки."
                )
            except TelegramSubscriber.DoesNotExist:
                await update.message.reply_text(
                    "Вы не были подписаны на уведомления.\n"
                    "Используйте /start для подписки."
                )

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("stop", stop))

        self.stdout.write(
            self.style.SUCCESS("Бот запущен. Нажмите Ctrl+C для остановки.")
        )

        # Запуск бота
        application.run_polling()