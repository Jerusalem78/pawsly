# Pawsly

Учебный fullstack-проект сервиса поиска ситтера для домашних животных. Владелец может разместить объявление об уходе за питомцем, а ситтер — откликнуться на него. В проекте есть frontend на React и TypeScript и backend API на FastAPI с PostgreSQL.

## Технологии

**Frontend:** React 18, TypeScript, Vite, React Router, Tailwind CSS.

**Backend:** Python 3.10+, FastAPI, SQLAlchemy (async), Alembic, PostgreSQL, JWT.

## Структура проекта

```text
.
├── backend/
│   ├── migrations/       # миграции Alembic
│   ├── src/
│   │   ├── core/         # настройки, БД, безопасность и общая логика
│   │   ├── models/       # модели SQLAlchemy
│   │   ├── repositories/ # работа с данными
│   │   ├── routers/      # маршруты API
│   │   ├── schemas/      # схемы Pydantic
│   │   └── services/     # бизнес-логика
│   └── pyproject.toml
├── frontend/
│   └── pawsly/           # приложение React + Vite
└── makefile
```

## Запуск проекта

### Требования

- Python 3.10 или новее и [uv](https://docs.astral.sh/uv/)
- Node.js и npm
- PostgreSQL

### Настройка backend

Перейдите в `backend`, создайте файл `.env` на основе переменных ниже и укажите параметры своей базы данных:

```env
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=your_password
DATABASE_NAME=pawsly
DATABASE_HOST=localhost
DATABASE_PORT=5432
SECRET_KEY=replace_with_a_long_random_secret
```

Установите зависимости и запустите API:

```bash
cd backend
uv sync
uv run uvicorn src.main:app --reload
```

После запуска документация API доступна по адресу [http://localhost:8000/docs](http://localhost:8000/docs).

### Запуск frontend

В другом терминале выполните:

```bash
cd frontend/pawsly
npm install
npm run dev
```

Vite выведет локальный адрес приложения в терминале.


