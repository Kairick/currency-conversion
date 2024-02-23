FROM python:3.11.3

WORKDIR /app/src

COPY ./src /app/src
COPY poetry.lock pyproject.toml /app/src/

RUN apt-get update && apt-get install -y build-essential
RUN apt-get install -y wait-for-it

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-dev

EXPOSE 8000