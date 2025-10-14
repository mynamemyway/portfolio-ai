# Dockerfile
FROM python:3.12-slim

# Установим зависимости ОС, если вдруг понадобятся (для некоторых пакетов)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Копируем зависимости и устанавливаем
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем код — сохраняем структуру!
COPY app ./app
COPY main.py .
COPY assets ./assets

# Владелец не требуется (работаем от root, но можно добавить non-root user при желании)

CMD ["python", "main.py"]