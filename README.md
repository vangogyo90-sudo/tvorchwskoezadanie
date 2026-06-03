# Kittygram — Health Passport

Коротко

Kittygram Health Passport — REST API для учёта питомцев: коты, паспорта здоровья, медицинские записи, клиники и врачи. Поддерживаются фильтрация, поиск и постраничная навигация. API документирован через Swagger/Redoc. Проект готов к развёртыванию в Docker.

Цель

Централизовать медицинскую историю питомца, упростить взаимодействие владельца и ветеринара и автоматизировать уведомления о предстоящих датах.

Быстрый старт (локально)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # заполните значения
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Docker (рекомендуется)

```bash
docker compose up --build -d
# после первого запуска создайте суперпользователя внутри контейнера
docker compose exec web python manage.py createsuperuser
```

Файл `.env.example` содержит основные переменные окружения (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `SQLITE_NAME`).

Основные эндпоинты (выборка)

- `GET /api/cats/` — полный список котов (unpaginated)
- `GET /api/cats/paginated/?page=1` — пагинированный список
- `GET /api/cats/search/?search=term` — поиск

- `GET /api/health-passports/` — список паспортов
- `GET /api/health-passports/paginated/` — пагинация
- `GET /api/health-passports/search/?search=term` — поиск

- `GET /api/health-records/` — список медицинских записей
- `GET /api/health-records/paginated/` — пагинация
- `GET /api/health-records/search/?search=term` — поиск
- `POST /api/health-records/{id}/complete/` — пометить запись как выполненную (custom action)

- `GET /api/clinics/`, `GET /api/doctors/` и соответствующие `paginated` / `search` действия.

Примеры использования

Создание медицинской записи (пример):

```bash
curl -u admin:password -X POST "http://127.0.0.1:8000/api/health-records/" \
  -H "Content-Type: application/json" \
  -d '{"passport": 1, "record_type": "vaccine", "title": "Вакцинация", "event_date": "2026-05-10", "next_due_date": "2027-05-10"}'
```

Пометить запись как выполненную:

```bash
curl -u admin:password -X POST "http://127.0.0.1:8000/api/health-records/1/complete/"
```

Документация

- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- ReDoc: `http://127.0.0.1:8000/api/redoc/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`

Требования реализации (кратко, выполнено)

- Новые модели: `HealthPassport`, `HealthRecord`, `Clinic`, `Doctor`.
- Минимум 4 новых эндпоинта: `health-passports`, `health-records`, `clinics`, `doctors` (+paginated/search).
- Кастомное действие: `POST /api/health-records/{id}/complete/`.
- Права доступа: владельцы, создатели, модераторы (staff) — реализованы в `health/permissions.py`.
- Валидации: `next_due_date >= event_date`; запрет дублирующих записей одного типа в один день для одного паспорта.
- Фильтрация и пагинация: есть фильтры по датам и paginated action.
- Документация: Swagger/Redoc через drf-spectacular.
- Секреты через `.env` (`.env.example` присутствует).

Контакты и поддержка

Описания эндпоинтов и примеры запросов находятся в Swagger UI и в коде сериализаторов/ViewSet. Для вопросов — откройте issue в репозитории.
