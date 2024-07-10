FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim AS builder

LABEL "Project"="sample"
LABEL "Organisation"="ANORA"

# Set the working directory
WORKDIR /app

# Copy the poetry.lock and pyproject.toml files
COPY pyproject.toml poetry.lock /app/

# Install dependencies using Poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Copy the FastAPI project files
COPY ./app /app/
