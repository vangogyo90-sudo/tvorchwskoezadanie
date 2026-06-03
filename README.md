# Kittygram Health Passport

Django REST Framework приложение для учета котов, паспортов здоровья, медицинских записей, пользователей и ролей.

## Что добавлено

- Новый веб-интерфейс и отдельные окна для ролей: владелец, ветеринар, администратор.
- Профиль пользователя с ролью, телефоном, клиникой и заметками.
- Таблица пользователей в административном окне и API `/api/users/`.
- CRUD для котов, паспортов здоровья и медицинских записей.
- Swagger UI, Redoc и OpenAPI schema через `drf-spectacular`.
- Фильтрация, поиск, сортировка и пагинация DRF.

## Роли

| Роль | Возможности |
| --- | --- |
| Владелец | Просматривает свои данные и добавляет своего питомца. |
| Ветеринар | Видит всех пациентов, паспорта и медицинские записи, может создавать записи. |
| Администратор | Управляет пользователями через API, видит все данные и таблицу пользователей. |

Суперпользователь и staff автоматически получают роль администратора.

## Запуск локально

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Главные страницы:

- Web dashboard: `http://127.0.0.1:8000/`
- Django Admin: `http://127.0.0.1:8000/admin/`
- Swagger: `http://127.0.0.1:8000/api/docs/`
- Redoc: `http://127.0.0.1:8000/api/redoc/`
- Schema: `http://127.0.0.1:8000/api/schema/`

## Таблица эндпоинтов

| URL | Методы | Доступ | Назначение |
| --- | --- | --- | --- |
| `/` | GET | Авторизованный/гость | Главная страница / дашборд (redir по роли при авторизации). |
| `/owner/` | GET | Владелец | Окно владельца с его котами и записями. |
| `/vet/` | GET | Ветеринар | Вет-интерфейс по пациентам. |
| `/admin-panel/` | GET | Администратор | Таблица пользователей и статистика. |
| `/api/users/` | GET/POST | Администратор | Список и создание пользователей. |
| `/api/users/{id}/` | GET/PATCH/PUT/DELETE | Администратор | Детальная работа с пользователем. |

| `/api/cats/` | GET/POST | Авторизованные | Список котов (unpaginated) / создать кота. |
| `/api/cats/paginated/` | GET | Авторизованные | Пагинированный список котов. |
| `/api/cats/search/` | GET | Авторизованные | Поиск котов (`?search=...`). |
| `/api/cats/{id}/` | GET/PATCH/PUT/DELETE | Авторизованные | Детали/редактирование/удаление кота. |

| `/api/health-passports/` | GET/POST | Авторизованные | Список паспортов (unpaginated) / создать паспорт. |
| `/api/health-passports/paginated/` | GET | Авторизованные | Пагинация паспортов. |
| `/api/health-passports/search/` | GET | Авторизованные | Поиск паспортов (`?search=...`). |
| `/api/health-passports/{id}/` | GET/PATCH/PUT/DELETE | Авторизованные | Детали/редактирование паспорта. |
| `/api/health-passports/upcoming/` | GET | Авторизованные | Ближайшие события по `next_due_date`. |

| `/api/health-records/` | GET/POST | Авторизованные | Список медицинских записей (unpaginated) / создать запись. |
| `/api/health-records/paginated/` | GET | Авторизованные | Пагинация записей. |
| `/api/health-records/search/` | GET | Авторизованные | Поиск/фильтрация записей. |
| `/api/health-records/{id}/` | GET/PATCH/PUT/DELETE | Авторизованные | Детали/редактирование записи. |
| `/api/health-records/upcoming/` | GET | Авторизованные | Записи с будущим сроком. |

| `/api/clinics/` | GET/POST | Авторизованные | Список клиник / создать клинику. |
| `/api/clinics/paginated/` | GET | Авторизованные | Пагинация клиник. |
| `/api/clinics/search/` | GET | Авторизованные | Поиск клиник. |
| `/api/clinics/{id}/` | GET/PATCH/PUT/DELETE | Авторизованные | Детали/редактирование клиники. |

| `/api/doctors/` | GET/POST | Авторизованные | Список врачей / создать врача. |
| `/api/doctors/paginated/` | GET | Авторизованные | Пагинация врачей. |
| `/api/doctors/search/` | GET | Авторизованные | Поиск врачей. |
| `/api/doctors/{id}/` | GET/PATCH/PUT/DELETE | Авторизованные | Детали/редактирование врача. |

| `/api/docs/` | GET | Все | Swagger UI (public). |
| `/api/redoc/` | GET | Все | ReDoc (public). |
| `/api/schema/` | GET | Все | OpenAPI schema (YAML/JSON). |

## Примеры запросов

Во всех API-примерах используется Basic Auth:

```bash
curl -u admin:password http://127.0.0.1:8000/api/cats/
```

### Создать пользователя

`POST /api/users/`

```json
{
  "username": "vet",
  "email": "vet@example.com",
  "first_name": "Анна",
  "last_name": "Иванова",
  "password": "strong-pass-123",
  "profile": {
    "role": "veterinarian",
    "phone": "+7 900 000-00-00",
    "clinic": "Добрый ветеринар"
  }
}
```

Ответ `201 Created`:

```json
{
  "id": 2,
  "username": "vet",
  "email": "vet@example.com",
  "first_name": "Анна",
  "last_name": "Иванова",
  "is_active": true,
  "is_staff": false,
  "date_joined": "2026-05-10T12:00:00Z",
  "profile": {
    "role": "veterinarian",
    "role_display": "Ветеринар",
    "phone": "+7 900 000-00-00",
    "clinic": "Добрый ветеринар",
    "notes": "",
    "created_at": "2026-05-10T12:00:00Z",
    "updated_at": "2026-05-10T12:00:00Z"
  }
}
```

### Создать кота

`POST /api/cats/`

```json
{
  "name": "Муся",
  "birth_date": "2022-04-12",
  "sex": "female",
  "breed": "Сибирская",
  "color": "дымчатый"
}
```

Ответ `201 Created`:

```json
{
  "id": 1,
  "owner": "owner",
  "name": "Муся",
  "birth_date": "2022-04-12",
  "sex": "female",
  "breed": "Сибирская",
  "color": "дымчатый",
  "created_at": "2026-05-10T12:01:00Z",
  "updated_at": "2026-05-10T12:01:00Z"
}
```

### Создать паспорт здоровья

`POST /api/health-passports/`

```json
{
  "cat_id": 1,
  "microchip_number": "643000000000001",
  "blood_type": "a",
  "sterilized": true,
  "weight_kg": "4.20",
  "allergies": "Нет",
  "chronic_conditions": "Нет",
  "veterinarian_name": "Иванова А.А.",
  "clinic_phone": "+7 900 000-00-00",
  "emergency_notes": "При отказе от еды связаться с клиникой."
}
```

Ответ `201 Created`:

```json
{
  "id": 1,
  "cat": {
    "id": 1,
    "owner": "owner",
    "name": "Муся",
    "birth_date": "2022-04-12",
    "sex": "female",
    "breed": "Сибирская",
    "color": "дымчатый",
    "created_at": "2026-05-10T12:01:00Z",
    "updated_at": "2026-05-10T12:01:00Z"
  },
  "microchip_number": "643000000000001",
  "blood_type": "a",
  "sterilized": true,
  "weight_kg": "4.20",
  "allergies": "Нет",
  "chronic_conditions": "Нет",
  "veterinarian_name": "Иванова А.А.",
  "clinic_phone": "+7 900 000-00-00",
  "emergency_notes": "При отказе от еды связаться с клиникой.",
  "records_count": 0,
  "upcoming_count": 0,
  "created_at": "2026-05-10T12:02:00Z",
  "updated_at": "2026-05-10T12:02:00Z"
}
```

### Создать медицинскую запись

`POST /api/health-records/`

```json
{
  "passport_id": 1,
  "record_type": "vaccination",
  "title": "Комплексная вакцинация",
  "event_date": "2026-05-10",
  "next_due_date": "2027-05-10",
  "clinic": "Добрый ветеринар",
  "doctor": "Иванова А.А.",
  "weight_kg": "4.20",
  "description": "Плановая вакцинация, реакция спокойная."
}
```

Ответ `201 Created`:

```json
{
  "id": 1,
  "cat": {
    "id": 1,
    "name": "Муся"
  },
  "created_by": "vet",
  "record_type": "vaccination",
  "title": "Комплексная вакцинация",
  "event_date": "2026-05-10",
  "next_due_date": "2027-05-10",
  "clinic": "Добрый ветеринар",
  "doctor": "Иванова А.А.",
  "weight_kg": "4.20",
  "description": "Плановая вакцинация, реакция спокойная.",
  "created_at": "2026-05-10T12:03:00Z",
  "updated_at": "2026-05-10T12:03:00Z"
}
```

### Получить будущие события

`GET /api/health-records/upcoming/?ordering=next_due_date`

Ответ `200 OK`:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "cat": {
        "id": 1,
        "name": "Муся"
      },
      "created_by": "vet",
      "record_type": "vaccination",
      "title": "Комплексная вакцинация",
      "event_date": "2026-05-10",
      "next_due_date": "2027-05-10",
      "clinic": "Добрый ветеринар",
      "doctor": "Иванова А.А.",
      "weight_kg": "4.20",
      "description": "Плановая вакцинация, реакция спокойная.",
      "created_at": "2026-05-10T12:03:00Z",
      "updated_at": "2026-05-10T12:03:00Z"
    }
  ]
}
```

## Фильтрация и поиск

Примеры:

```bash
curl -u owner:password "http://127.0.0.1:8000/api/cats/?search=Муся&ordering=name"
curl -u vet:password "http://127.0.0.1:8000/api/health-passports/?has_microchip=true"
curl -u vet:password "http://127.0.0.1:8000/api/health-records/?record_type=vaccination&date_from=2026-01-01"
```

## Docker

```bash
docker compose up -d --build
docker compose exec web python manage.py createsuperuser
```

Контейнер использует SQLite в Docker volume `sqlite_data`, поэтому данные сохраняются между перезапусками. Приложение будет доступно на `http://127.0.0.1:8000/`.

Полезные команды:

```bash
docker compose ps
docker compose logs -f web
docker compose exec web python manage.py test
docker compose down
```

## Проверка

```bash
python manage.py test
python manage.py spectacular --file schema.yml
```
# tvorchwskoezadanie
