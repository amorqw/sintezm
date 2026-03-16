# Синтез М - Развертывание проекта

Этот проект представляет собой Django-приложение для сайта компании "Синтез М", предоставляющей услуги по обслуживанию танк-контейнеров и бензовозов.

**🚀 Рекомендуемый способ развертывания: [Railway](https://railway.app)** - самый простой и быстрый вариант для Django проектов!

## Функции

- 🌐 **Веб-сайт**: Информационные страницы, каталог услуг, контактная форма
- 📝 **Заявки**: Форма подачи заявок на услуги с автоматическими уведомлениями
- 🤖 **Telegram бот**: Уведомления подписчикам о новых заявках
- 🐳 **Docker**: Готовая конфигурация для развертывания
- ☁️ **Vercel**: Поддержка бессерверного развертывания

## Структура проекта

```
sintez_m/
├── apps/                          # Приложения Django
│   ├── applications/              # Заявки на услуги
│   ├── catalog/                   # Каталог товаров/услуг
│   ├── core/                      # Основное приложение
│   └── services/                  # Услуги
├── config/                        # Конфигурация Django
│   ├── settings/                  # Настройки по окружениям
│   └── urls.py                    # Основные URL
├── media/                         # Медиафайлы
├── static/                        # Статические файлы
├── templates/                     # Шаблоны
├── logs/                          # Логи
├── nginx/                         # Конфигурация Nginx
├── run_bot.py                     # Скрипт Telegram бота
├── vercel.json                    # Конфигурация Vercel
├── docker-compose.yml             # Docker Compose
├── Dockerfile                     # Docker образ
├── manage.py                      # Django CLI
└── requirements.txt               # Зависимости Python
```

## Требования

- **Railway** (рекомендуется) или Docker для production развертывания
- Python 3.11+ для локальной разработки
- PostgreSQL (Railway предоставляет автоматически)
- Аккаунт GitHub для развертывания

## Telegram бот

Проект включает Telegram бота для уведомлений о новых заявках. Бот позволяет:
- Подписываться на уведомления командой `/start`
- Отписываться командой `/stop`
- Получать автоматические уведомления о новых заявках

**Настройка бота:**
1. Создайте бота через [@BotFather](https://t.me/botfather) в Telegram
2. Получите токен бота
3. Добавьте токен в переменные окружения: `TELEGRAM_BOT_TOKEN=ваш_токен`

## Развертывание

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd sintez_m
```

### 2. Настройка переменных окружения

Создайте файл `.env` в корне проекта на основе `.env.example`:

**Для Railway (рекомендуется):**
```env
# Django
SECRET_KEY=ваш-секретный-ключ
DEBUG=False
ALLOWED_HOSTS=ваш-домен.railway.app

# Telegram бот (опционально, для уведомлений о заявках)
TELEGRAM_BOT_TOKEN=ваш_токен_бота
```

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

**Важно:** Сгенерируйте новый `SECRET_KEY` с помощью:
```bash
python generate_secret.py
```
или `python -c "import secrets; print(secrets.token_urlsafe(50))"`

### 3. Развертывание на Railway

Railway - самый простой способ развертывания Django приложений:

1. **Регистрация:**
   - Перейдите на [railway.app](https://railway.app)
   - Создайте аккаунт (есть бесплатный тариф)

2. **Создание проекта:**
   - Нажмите "New Project" → "Deploy from GitHub"
   - Подключите ваш GitHub аккаунт
   - Выберите репозиторий с проектом

3. **Railway автоматически:**
   - Обнаружит Python/Django проект
   - Установит зависимости из `requirements.txt`
   - Создаст PostgreSQL базу данных
   - Настроит домен (например, `your-app.railway.app`)

4. **Настройте переменные окружения** в Railway Dashboard → Variables:
   ```
   SECRET_KEY=ваш-секретный-ключ
   DEBUG=False
   ALLOWED_HOSTS=ваш-домен.railway.app
   TELEGRAM_BOT_TOKEN=ваш_токен_бота (опционально)
   ```

5. **Готово!** Приложение будет доступно по сгенерированному URL

**Примечание:** Railway использует файлы `Procfile`, `runtime.txt` и `requirements.txt` для автоматической настройки.

5. **Переразверните**:
   ```bash
   vercel --prod
   ```

### 4. Локальный запуск (для разработки)

```bash
# Установите зависимости
pip install -r requirements.txt

# Примените миграции
python manage.py migrate

# Запустите сервер
python manage.py runserver
```

**Запуск Telegram бота (в отдельном терминале):**
```bash
python run_bot.py
```

**Тестирование бота:**
- Найдите бота в Telegram по имени
- Отправьте `/start` для подписки
- Создайте тестовую заявку через веб-интерфейс
- Проверьте получение уведомления в Telegram
```

Сервер будет доступен по адресу: http://localhost:8000

### 5. Запуск с Docker Compose

```bash
docker-compose up -d
```

Это запустит:
- Django-приложение (Gunicorn, 3 воркера)
- PostgreSQL базу данных
- Nginx веб-сервер
- **Telegram-бот** (автоматически, если задан `TELEGRAM_BOT_TOKEN`)

### 6. Миграции и статические файлы

При первом запуске контейнеры автоматически выполнят:
- Миграции БД (`python manage.py migrate`)
- Сбор статических файлов (`python manage.py collectstatic`)

Если нужно вручную:
```bash
docker-compose exec app python manage.py migrate
docker-compose exec app python manage.py collectstatic --noinput
```

### 7. Настройка Telegram бота

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

### 8. Создание суперпользователя (опционально)

```bash
docker-compose exec app python manage.py createsuperuser
```

### 9. Настройка SSL (рекомендуется)

1. Получите SSL-сертификаты (Let's Encrypt или другие).
2. Поместите их в `nginx/ssl/`:
   - `fullchain.pem` (сертификат)
   - `privkey.pem` (приватный ключ)
3. Nginx настроен для HTTPS (порт 443).

Если SSL не нужен, измените `nginx/nginx.conf` для HTTP-only.

### 10. Мониторинг

- Логи приложения: `docker-compose logs app`
- Логи Nginx: `docker-compose logs nginx`
- Логи БД: `docker-compose logs db`

### 11. Обновление

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

## Поддержка

Если у вас возникли проблемы с развертыванием или работой приложения:

1. **Проверьте логи**:
   ```bash
   docker-compose logs -f app
   ```

2. **Проверьте статус контейнеров**:
   ```bash
   docker-compose ps
   ```

3. **Перезапустите сервисы**:
   ```bash
   docker-compose restart
   ```

4. **Обновите образы**:
   ```bash
   docker-compose pull && docker-compose up -d
   ```

Для вопросов по коду или развертыванию создайте issue в репозитории.