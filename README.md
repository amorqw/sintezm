# Синтез М - Развертывание проекта

Этот проект представляет собой Django-приложение для сайта компании "Синтез М", предоставляющей услуги по обслуживанию танк-контейнеров и бензовозов.

## Требования

- Docker и Docker Compose
- Доменное имя (опционально, для SSL)

## Развертывание

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd sintez_m
```

### 2. Настройка переменных окружения

Создайте файл `.env` в корне проекта на основе `.env.example`:

**Для локальной разработки:**
```env
# Django
SECRET_KEY=ваш-секретный-ключ
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# База данных (SQLite для разработки)
DATABASE_URL=sqlite:///db.sqlite3

# Telegram бот (опционально, для тестирования)
TELEGRAM_BOT_TOKEN=ваш_токен_бота
```

**Для production с Docker:**
```env
# Django
SECRET_KEY=ваш-секретный-ключ
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# База данных
POSTGRES_DB=sintez_db
POSTGRES_USER=sintez_user
POSTGRES_PASSWORD=ваш-пароль-db
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Telegram бот (для уведомлений о заявках)
TELEGRAM_BOT_TOKEN=ваш_токен_бота

# Другие настройки
SITE_NAME=Синтез М
```

**Важно:** Сгенерируйте новый `SECRET_KEY` с помощью `python -c "import secrets; print(secrets.token_urlsafe(50))"`

### 2.1. Локальный запуск (для разработки)

```bash
# Установите зависимости
pip install -r requirements.txt

# Примените миграции
python manage.py migrate

# Запустите сервер
python manage.py runserver
```

Сервер будет доступен по адресу: http://localhost:8000

### 3. Запуск с Docker Compose

### 3. Запуск с Docker Compose

```bash
docker-compose up -d
```

Это запустит:
- Django-приложение (Gunicorn, 3 воркера)
- PostgreSQL базу данных
- Nginx веб-сервер
- **Telegram-бот** (автоматически, если задан `TELEGRAM_BOT_TOKEN`)

### 4. Миграции и статические файлы

При первом запуске контейнеры автоматически выполнят:
- Миграции БД (`python manage.py migrate`)
- Сбор статических файлов (`python manage.py collectstatic`)

Если нужно вручную:
```bash
docker-compose exec app python manage.py migrate
docker-compose exec app python manage.py collectstatic --noinput
```

### 5. Настройка Telegram бота

1. Создайте бота через [@BotFather](https://t.me/botfather) в Telegram и получите токен.
2. Добавьте `TELEGRAM_BOT_TOKEN=ваш_токен` в файл `.env`.
3. **Бот запустится автоматически** при `docker-compose up -d`.

Пользователи могут подписываться на уведомления командой `/start` и отписываться `/stop`.

При создании новой заявки на сайте все подписчики получат уведомление в Telegram.

Если нужно запустить бота отдельно для тестирования:
```bash
docker-compose exec app python manage.py run_telegram_bot
```
Или для локальной разработки:
```bash
python manage.py run_telegram_bot
```

### 6. Создание суперпользователя (опционально)

```bash
docker-compose exec app python manage.py createsuperuser
```

### 6. Настройка SSL (рекомендуется)

1. Получите SSL-сертификаты (Let's Encrypt или другие).
2. Поместите их в `nginx/ssl/`:
   - `fullchain.pem` (сертификат)
   - `privkey.pem` (приватный ключ)
3. Nginx настроен для HTTPS (порт 443).

Если SSL не нужен, измените `nginx/nginx.conf` для HTTP-only.

### 7. Мониторинг

- Логи приложения: `docker-compose logs app`
- Логи Nginx: `docker-compose logs nginx`
- Логи БД: `docker-compose logs db`

### 8. Обновление

```bash
git pull
docker-compose down
docker-compose up --build -d
```

### Структура проекта

- `apps/` - Django приложения (catalog, services, etc.)
- `config/` - Настройки Django
- `static/` - Статические файлы (CSS, JS, изображения)
- `templates/` - HTML-шаблоны
- `nginx/` - Конфигурация Nginx
- `Dockerfile` - Сборка образа приложения
- `docker-compose.yml` - Оркестрация сервисов

### Переменные окружения

Полный список переменных в `config/settings/production.py`.

### Безопасность

- Не коммитите `.env` в Git (добавьте в `.gitignore`)
- Используйте сильные пароли
- Регулярно обновляйте зависимости
- Настройте бэкапы БД

### Поддержка

Если возникли проблемы, проверьте логи и настройки в `.env`.