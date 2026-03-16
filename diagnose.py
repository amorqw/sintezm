#!/usr/bin/env python
"""
Диагностический скрипт для проверки развертывания на Railway
"""
import os
import sys
import django
from pathlib import Path

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
sys.path.insert(0, str(Path(__file__).parent))

try:
    django.setup()
    print("✅ Django setup successful")

    # Проверка импорта моделей
    from django.contrib.auth.models import User
    print("✅ Django models import successful")

    # Проверка базы данных
    from django.db import connection
    cursor = connection.cursor()
    print("✅ Database connection successful")

    # Проверка статических файлов
    from django.contrib.staticfiles.storage import staticfiles_storage
    print(f"✅ Static files storage: {staticfiles_storage.__class__.__name__}")

    # Проверка переменных окружения
    print(f"✅ DEBUG: {os.getenv('DEBUG', 'Not set')}")
    print(f"✅ SECRET_KEY: {'Set' if os.getenv('SECRET_KEY') else 'Not set'}")
    print(f"✅ DATABASE_URL: {'Set' if os.getenv('DATABASE_URL') else 'Not set'}")
    print(f"✅ ALLOWED_HOSTS: {os.getenv('ALLOWED_HOSTS', 'Not set')}")

    # Проверка Railway переменных
    railway_vars = [var for var in os.environ.keys() if var.startswith('RAILWAY')]
    if railway_vars:
        print(f"✅ Railway variables found: {railway_vars}")
    else:
        print("⚠️  No Railway variables found")

    print("\n🎉 All checks passed! Application should work on Railway.")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)