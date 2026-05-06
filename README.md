 Habit Tracker API

[![Django](https://img.shields.io/badge/Django-6.0.4-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.17.1-red.svg)](https://www.django-rest-framework.org/)
[![Celery](https://img.shields.io/badge/Celery-5.6.3-brightgreen.svg)](https://docs.celeryq.dev/)
[![Coverage](https://img.shields.io/badge/Coverage-84%25-brightgreen.svg)](https://pytest-cov.readthedocs.io/)

Бэкенд-часть SPA веб-приложения для трекера полезных привычек. Реализован на Django REST Framework с использованием Celery для отложенных задач и Telegram бота для отправки уведомлений.

## 📋 Описание проекта

Проект представляет собой API для управления привычками, вдохновленный книгой Джеймса Клира «Атомные привычки». Пользователи могут создавать полезные и приятные привычки, получать напоминания о них в Telegram и делиться привычками с другими пользователями.

### Основные возможности

- Регистрация и JWT-авторизация пользователей
- CRUD операции с привычками
- Пагинация списка привычек (5 привычек на страницу)
- Разграничение прав доступа (пользователь видит только свои привычки)
- Публичные привычки (доступны всем)
- Валидация данных привычек (длительность, периодичность, связанные привычки)
- Отложенные задачи Celery для отправки напоминаний
- Telegram бот для получения уведомлений
- Документация API (Swagger/ReDoc)

## 🚀 Быстрый старт

### Требования

- Python 3.12+
- PostgreSQL
- Redis (или Memurai для Windows)
- Telegram Bot Token (получить у [@BotFather](https://t.me/BotFather))

### Установка

**1. Клонировать репозиторий:**
```bash
git clone <repository-url>
cd Habbit_tracker
```
**2. Установить зависимости через Poetry:**
```bash
poetry install
```
**3. Создать файл окружения:**

```bash
cp .env.sample .env
```
#### Отредактировать .env, указав свои значения
**4. Применить миграции:**
```bash
poetry run python manage.py migrate
```
**5. Создать суперпользователя:**

```bash
poetry run python manage.py createsuperuser
```
**6. Запустить Redis (WSL или Memurai):**
**7. Запустить Celery Worker:**
```bash
poetry run celery -A config worker --loglevel=info --pool=solo
```
**8. Запустить Celery Beat (планировщик):**
```bash
poetry run celery -A config beat --loglevel=info
```
**9. Запустить Telegram бота:**
```bash
poetry run python manage.py run_bot
```
**10. Запустить Django сервер:**
```bash
poetry run python manage.py runserver
```
## 📚 Документация API
Документация доступна после запуска сервера по адресам:

Swagger UI: http://localhost:8000/swagger/

ReDoc: http://localhost:8000/redoc/

Admin панель: http://localhost:8000/admin/

### **Эндпоинты API:**

| Метод | URL | Описание | Доступ |
|-------|-----|----------|--------|
| POST | /api/register/ | Регистрация пользователя | Все |
| POST | /api/token/ | Получение JWT токена | Все |
| POST | /api/token/refresh/ | Обновление токена | Все |
| GET | /api/habits/ | Список привычек пользователя | Только авторизованные |
| POST | /api/habits/ | Создание привычки | Только авторизованные |
| GET | /api/habits/{id}/ | Детали привычки | Владелец |
| PUT/PATCH | /api/habits/{id}/ | Обновление привычки | Владелец |
| DELETE | /api/habits/{id}/ | Удаление привычки | Владелец |
| GET | /api/habits/public/ | Список публичных привычек | Все |


### Примеры запросов
#### Регистрация пользователя:

``` bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "email": "user@example.com", "password": "securepass"}'
```
Получение токена:

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "securepass"}'
```
Создание привычки:

```bash
curl -X POST http://localhost:8000/api/habits/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"place": "Дом", "time": "09:00", "action": "Сделать зарядку", "duration": 60, "periodicity": 1}'
```
## 🤖 Telegram Бот
### Настройка бота:
Напишите @BotFather в Telegram

Отправьте команду /newbot

Укажите имя бота (например, My Habit Tracker Bot)

Укажите username бота (должен заканчиваться на _bot)

Скопируйте полученный токен в .env:
```text
TELEGRAM_BOT_TOKEN=ваш_токен
```
### Использование бота
Запустите бота:
```bash
python manage.py run_bot
```

В Telegram найдите своего бота и отправьте /start

Бот привяжет ваш аккаунт к пользователю в системе

Теперь вы будете получать напоминания о привычках

## 🧪 Тестирование
Запуск тестов
### Запуск всех тестов
```bash
pytest -v
```
### Запуск с проверкой покрытия
```bash
pytest --cov=habits --cov=users --cov-report=term --cov-report=html
```
#### Покрытие кода
Итоговое покрытие: 84% (превышает требуемые 80%)
| Компонент             |Покрытие|
|-----------------------|--------|
| habits/models.py      | 100%   |
| habits/serializers.py | 88%    |
| habits/views.py       | 93%    |
| users/models.py       | 90%    |
| users/serializers.py  | 91%    |
| users/views.py        | 100%   |
| **Общее**             | **84%**|

## 🛠 Технологии
Django 6.0.4 — веб-фреймворк

Django REST Framework 3.17.1 — создание API

Django REST Framework SimpleJWT — JWT авторизация

Celery 5.6.3 — отложенные задачи

Redis — брокер сообщений

PostgresSQL — база данных

pyTelegramBotAPI — Telegram бот

pytest — тестирование

drf-yasg — документация API

django-cors-headers — CORS настройки