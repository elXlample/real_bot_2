# Базовый образ Python
FROM python:3.11-slim

# Создаём рабочую папку
WORKDIR /app

# Копируем файлы
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .