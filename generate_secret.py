#!/usr/bin/env python
"""
Скрипт для генерации SECRET_KEY для Django
"""
import secrets

secret_key = secrets.token_urlsafe(50)
print(f"SECRET_KEY={secret_key}")