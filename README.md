# GLOSSARY APP

## How to

### Start app

    uvicorn glossary.application.app:create_app --factory --port 8080

### Run tests

    pytest glossary/tests/test_session.py

### Migration

    alembic revision --autogenerate -m "my new migration"
    alembic upgrade head

## Docker

In container port: **8080**

### Env example

    SECRET_KEY=SUPERSECRETKEY
    DB_HOST=127.0.0.1
    DB_PORT=5432
    DB_USER=jayse
    DB_PASSWORD=test
    DB_NAME=glossary_app_db

### Run docker

    docker build -t glossary_backend .
    docker run -d -t --name glossary_backend_container --env-file env --network host glossary_backend

In progress..
