FROM python:3.11

WORKDIR /app

# Копируем файлы проекта
COPY .. .

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y redis-tools
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Устанавливаем переменные окружения
ENV REDIS_URL=redis://redis:6379/0
ENV REDIS_HOST=redis

# Создаем скрипт запуска
RUN echo '#!/bin/bash\n\
celery -A bike_rental worker -l info &\n\
gunicorn bike_rental.wsgi:application --bind 127.0.0.1:8000\n'\
> /app/start.sh && chmod +x /app/start.sh

# Запускаем скрипт
CMD ["/app/start.sh"]