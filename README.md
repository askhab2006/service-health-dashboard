# 📊 Service Health Dashboard

Асинхронная система мониторинга доступности веб-сервисов. Проект позволяет отслеживать работоспособность сайтов в реальном времени, строить графики времени ответа и получать мгновенные уведомления в Telegram при сбоях.

## 🚀 Основные возможности
- **Автоматический мониторинг:** Фоновая проверка сервисов по расписанию (APScheduler).
- **Telegram Уведомления:** Мгновенные алерты при изменении статуса (UP/DOWN).
- **Интерактивные графики:** Визуализация времени ответа сервисов через Chart.js.
- **REST API:** Полноценное управление сервисами (CRUD) и результатами проверок.
- **Контейнеризация:** Быстрый запуск всей системы через Docker Compose.

## 🛠 Технологический стек
- **Язык:** Python 3.12
- **Framework:** FastAPI (Async)
- **Database:** SQLAlchemy 2.0, SQLite (aiosqlite)
- **Migrations:** Alembic
- **Frontend:** Jinja2, Bootstrap 5, Chart.js
- **Task Runner:** APScheduler
- **Async Client:** HTTPX
- **Infrastructure:** Docker, Docker Compose

## 📦 Как запустить

### 1. Клонирование репозитория
```bash
git clone https://github.com
cd service-health-dashboard