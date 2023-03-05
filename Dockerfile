# позволяет более явно указать версию используемого
# Dockerfile и увеличивает читаемость
# syntax=docker/dockerfile:1

#############################################
## docker for Zero Telegram Bot on AIOGram ##
#############################################
# Copyright (c) DNP LLC.

# Устанавливаем базовый образ Python версии 3.9
# Set the base image using Python ver.3.9
FROM python:3.9

# Указываем автора образа
MAINTAINER "bunta@home.lab"

# Определяем рабочую директорию для контейнера
# Set working directory
WORKDIR /usr/src/app

# Копируем requirements.txt внутрь образа
COPY requirements.txt ./

# Устанавливаем зависимости из файла requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы и папки из текущей директории внутрь образа
COPY . .

# Запуск команды при старте контейнера
# Run python3 with main.py on start
CMD ["python", "main.py"]
