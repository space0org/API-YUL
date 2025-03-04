FROM python:3.12-slim

# Install PostgreSQL client libraries and other dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . .

EXPOSE 5002

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5002", "--reload"]
