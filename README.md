# MASTERCARD Task API Assessment

FastAPI CRUD service for user-scoped task management.

## Goal

The project models a small task-list API where callers can create users and tasks, then read, update, and delete only their own records. Authentication is assumed to happen upstream, with the authenticated user identifier forwarded through the `RISKRECON-USER-ID` header.

## Stack

- FastAPI
- SQLAlchemy
- Alembic
- pytest
- Ruff

## Local Setup

```bash
python -m pip install -r requirements.txt
python -m pip install pytest ruff
```

## Run

```bash
uvicorn src.python_api.main:app --reload
```

The interactive API docs are available at `http://localhost:8000/docs`.

## Validation

```bash
ruff check .
pytest
```

## Assessment Scope

The original exercise asks for at least one of these enhancements:

- add email support to the `POST /users` route
- let a user fetch all of their tasks
- let a user edit one of their tasks
