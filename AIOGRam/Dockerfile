# Базовый образ
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем зависимости
RUN pip install --upgrade pip \
    && pip install poetry

# Копируем только файлы с зависимостями, чтобы воспользоваться кешированием слоев Docker
COPY pyproject.toml ./

# Устанавливаем зависимости с помощью poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# Копируем остальные файлы
COPY . .

# Команда для запуска вашего приложения
CMD ["python", "bot.py"]
