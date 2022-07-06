# GLOSSARY APP

## How to

    uvicorn glossary.application.app:create_app --factory --port 8080

### Migration

    alembic revision --autogenerate -m "my new migration"
    alembic upgrade head

## Docker

In container port: **8080**

```bash
docker build -t glossary_backend .

docker run -d --name glossary_backend_container --network host glossary_backend
```

In progress..
