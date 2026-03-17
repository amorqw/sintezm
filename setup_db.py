#!/usr/bin/env python
"""
Скрипт для настройки PostgreSQL базы данных
"""
import os
import sys
import subprocess
from pathlib import Path

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
sys.path.insert(0, str(Path(__file__).parent))

import django
django.setup()

from django.conf import settings
from django.core.management import execute_from_command_line

def create_database():
    """Создание базы данных PostgreSQL"""
    db_settings = settings.DATABASES['default']

    if db_settings['ENGINE'] != 'django.db.backends.postgresql':
        print("База данных не PostgreSQL, пропускаем создание")
        return

    db_name = db_settings['NAME']
    db_user = db_settings['USER']
    db_password = db_settings['PASSWORD']
    db_host = db_settings['HOST']
    db_port = db_settings['PORT']

    print(f"Создание базы данных: {db_name}")

    # Команда для создания базы данных
    cmd = f'psql -h {db_host} -p {db_port} -U {db_user} -c "CREATE DATABASE {db_name};"'

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, env={**os.environ, 'PGPASSWORD': db_password})
        if result.returncode == 0:
            print(f"✅ База данных {db_name} создана успешно")
        else:
            print(f"⚠️  База данных возможно уже существует: {result.stderr}")
    except Exception as e:
        print(f"❌ Ошибка создания базы данных: {e}")

def run_migrations():
    """Выполнение миграций"""
    print("Выполнение миграций...")
    execute_from_command_line(['manage.py', 'migrate'])

def create_superuser():
    """Создание суперпользователя"""
    print("Создание суперпользователя...")
    try:
        execute_from_command_line(['manage.py', 'createsuperuser', '--noinput', '--username', 'admin', '--email', 'admin@example.com'])
        print("✅ Суперпользователь создан (admin/admin)")
    except Exception as e:
        print(f"⚠️  Суперпользователь возможно уже существует: {e}")

if __name__ == '__main__':
    print("🚀 Настройка PostgreSQL базы данных для Django проекта")
    create_database()
    run_migrations()
    create_superuser()
    print("✅ Настройка завершена!")