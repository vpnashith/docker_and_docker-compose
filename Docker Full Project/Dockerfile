FROM tiangolo/uvicorn-gunicorn:python3.11-slim AS builder

LABEL "Project"="Validation Studio"
LABEL "Organisation"="ANORA"

# Set the working directory
WORKDIR /app/ValidationStudioCloud


# Copy the poetry.lock and pyproject.toml files
COPY pyproject.toml poetry.lock /app/ValidationStudioCloud/

# Install dependencies using Poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry lock && \
    poetry install --no-interaction --no-ansi

# Copy the FastAPI project files
COPY Project /app/ValidationStudioCloud/
