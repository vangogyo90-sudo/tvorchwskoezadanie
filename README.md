# Kittygram — Health Passport

Kittygram Health Passport — Django + DRF проект для учёта медицинской истории питомцев: коты, паспорта здоровья, медицинские записи, клиники, врачи и вакцинации.

Ключевые особенности
- REST API с CRUD для паспортов, записей, клиник, врачей, вакцин и введений вакцин.
- Фильтрация, поиск и пагинация для списков.
- Валидаторы для корректных дат и предотвращения дубликатов.
- OpenAPI документация (Swagger и ReDoc).
- Готов к запуску в Docker.

Быстрый старт (локально)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env  # заполните значения в .env
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

.env

Файл `.env.example` содержит необходимые переменные окружения: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `SQLITE_NAME`.

Основные API эндпоинты

- `GET /api/cats/`
- `GET /api/health-passports/`
- `GET /api/health-records/`
- `POST /api/health-records/{id}/complete/` — пометить запись как выполненную
- `GET /api/clinics/`, `GET /api/doctors/`
- `GET /api/vaccines/`, `GET /api/vaccine-administrations/`

Примеры запросов

Создание медицинской записи:

```bash
curl -u admin:password -X POST "http://127.0.0.1:8000/api/health-records/" \
  -H "Content-Type: application/json" \
  -d '{"passport": 1, "record_type": "vaccine", "title": "Вакцинация", "event_date": "2026-05-10", "next_due_date": "2027-05-10"}'
```

Добавление вакцины в каталог:

```bash
curl -u admin:password -X POST "http://127.0.0.1:8000/api/vaccines/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Rabies (RABVAC)", "manufacturer": "Acme Vaccines"}'
```

Запись введённой вакцины:

```bash
curl -u admin:password -X POST "http://127.0.0.1:8000/api/vaccine-administrations/" \
  -H "Content-Type: application/json" \
  -d '{"vaccine_id": 1, "passport_id": 1, "administered_at":"2026-05-10", "dose":"1ml"}'
```

Документация

- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- ReDoc: `http://127.0.0.1:8000/api/redoc/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`

Что добавлено по требованиям

- Новые модели: `HealthPassport`, `HealthRecord`, `Clinic`, `Doctor`, `Vaccine`, `VaccineAdministration`.
- Новые эндпоинты: `health-passports`, `health-records`, `clinics`, `doctors`, `vaccines`, `vaccine-administrations`.
- Кастомное действие: `POST /api/health-records/{id}/complete/`.
- Права: владельцы/создатели/модераторы реализованы в `health/permissions.py`.
- Валидации: `next_due_date >= event_date`; запрет дублирующих записей и дублирующих введений вакцин на ту же дату.
- Фильтрация и пагинация: реализованы для `health-records` и других списков.
- Секреты через `.env` (`.env.example` присутствует).

Поддержка и вклад

Откройте issue или pull request в репозитории для предложений и исправлений.

---
Автор и репозиторий: https://github.com/vangogyo90-sudo/tvorchwskoezadanie
