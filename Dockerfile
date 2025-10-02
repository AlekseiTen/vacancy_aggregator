# Используем Python 3.12 slim
FROM python:3.12-slim

# Установка системных пакетов
RUN apt-get update && apt-get install -y build-essential tzdata && rm -rf /var/lib/apt/lists/*

# Установка таймзоны (Москва)
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Создаём пользователя (для безопасности)
RUN useradd -m appuser

# Рабочая директория
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Права на папку приложения
RUN chown -R appuser:appuser /app

# Запуск от непользователя root
USER appuser

# Для корректного вывода логов Python
ENV PYTHONUNBUFFERED=1
