FROM python:3.9 as requirements-stage

WORKDIR /tmp

COPY ./requirements.txt /tmp/requirements.txt

FROM python:3.9

WORKDIR /app

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app/

CMD ["uvicorn", "--factory", "glossary.application.app:create_app", "--host", "127.0.0.1", "--port", "8080"]