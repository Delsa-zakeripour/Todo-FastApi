# Todo App (FastAPI)

A full-stack todo application built with **FastAPI**. Users can register, log in with JWT authentication, and manage their own todos through a web UI (Jinja2 + Bootstrap) or a REST API. Admins can see and delete every user's todos.

## Features

- User registration and login with **JWT** tokens (stored in an `access_token` cookie for the UI)
- Passwords hashed with **bcrypt**
- Create, read, update, and delete todos, scoped to their owner
- Admin role with access to all todos
- Change password and phone number
- Server-rendered pages with **Jinja2** templates and **Bootstrap 4**
- Database migrations with **Alembic**
- Tests with **pytest** against a separate SQLite test database

## Tech stack

| Layer      | Tools                                     |
| ---------- | ----------------------------------------- |
| Backend    | FastAPI, Starlette, Uvicorn               |
| Database   | SQLite (default), SQLAlchemy, Alembic     |
| Auth       | python-jose (JWT), passlib + bcrypt       |
| Frontend   | Jinja2, Bootstrap 4, vanilla JavaScript   |
| Testing    | pytest, FastAPI `TestClient`              |

Requires **Python 3.14+** and [uv](https://docs.astral.sh/uv/).

## Project structure

```
book-project-fastapi/
├── app/
│   ├── main.py          # FastAPI app, static files, router registration
│   ├── database.py      # SQLAlchemy engine and session
│   ├── models.py        # Users and Todos tables
│   ├── schema.py        # Pydantic request models
│   ├── router/
│   │   ├── auth.py      # register, login (token), login/register pages
│   │   ├── todos.py     # todo API and todo pages
│   │   ├── admin.py     # admin-only endpoints
│   │   └── users.py     # current user, password, phone number
│   ├── templates/       # Jinja2 HTML pages
│   └── static/          # CSS and JavaScript
├── alembic/             # database migrations
├── test/                # pytest tests
└── pyproject.toml
```

## Getting started

1. Install the dependencies:

   ```bash
   uv sync
   ```

2. Start the development server from the project root:

   ```bash
   uv run fastapi dev app/main.py
   ```

3. Open <http://127.0.0.1:8000>. You will be redirected to the todo page, or to the login page if you are not signed in.

The SQLite database (`todosapp.db`) is created automatically on first run.

Interactive API docs are available at <http://127.0.0.1:8000/docs>.

## Web pages

| URL                               | Page                  |
| --------------------------------- | --------------------- |
| `/auth/register-page`             | Create an account     |
| `/auth/login-page`                | Log in                |
| `/todo/todo-page`                 | Your todo list        |
| `/todo/add-todo`                  | Add a new todo        |
| `/todo/edit-todo-page/{todo_id}`  | Edit or delete a todo |

## API endpoints

Endpoints other than registration, login and health check need an `Authorization: Bearer <token>` header.

### Auth — `/auth`

| Method | Path          | Description                              |
| ------ | ------------- | ---------------------------------------- |
| POST   | `/auth/`      | Register a new user                      |
| POST   | `/auth/token` | Log in (form data) and get an access token |

### Todos — `/todo`

| Method | Path                   | Description             |
| ------ | ---------------------- | ----------------------- |
| GET    | `/todo/`               | List your todos         |
| GET    | `/todo/todo/{todo_id}` | Get one of your todos   |
| POST   | `/todo/todo`           | Create a todo           |
| PUT    | `/todo/todo/{todo_id}` | Update a todo           |
| DELETE | `/todo/todo/{todo_id}` | Delete a todo           |

### Users — `/user`

| Method | Path                               | Description               |
| ------ | ---------------------------------- | ------------------------- |
| GET    | `/user/`                           | Get the current user      |
| PUT    | `/user/password`                   | Change your password      |
| PUT    | `/user/phonenumber/{phone_number}` | Change your phone number  |

### Admin — `/admin` (admin role only)

| Method | Path                    | Description           |
| ------ | ----------------------- | --------------------- |
| GET    | `/admin/todos`          | List all todos        |
| DELETE | `/admin/todo/{todo_id}` | Delete any todo       |

### Other

| Method | Path      | Description   |
| ------ | --------- | ------------- |
| GET    | `/health` | Health check  |

## Database migrations

Create a migration after changing `app/models.py`:

```bash
uv run alembic revision -m "describe your change"
```

Apply migrations:

```bash
uv run alembic upgrade head
```

## Running tests

```bash
uv run pytest
```

Tests use their own database (`testdb.db`) and override the database and current-user dependencies, so they don't touch your real data.
