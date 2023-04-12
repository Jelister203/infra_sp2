FROM python:3.7-slim

# Создать директорию вашего приложения.
RUN mkdir /app

ENV token 12345

# Скопировать с локального компьютера файл зависимостей
# в директорию /app.
COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY . /app

# Сделать директорию /app рабочей директорией. 
WORKDIR /app

# Выполнить запуск сервера разработки при старте контейнера.
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ] 