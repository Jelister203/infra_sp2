# Учебный проект infra_sp2
### Описание
Этот проект может многое.
### Технологии
Python 3.7
Django 2.2.19
### Шаблон заполнения env-файла
- Указываем, что работаем с PostgreSQL:
```
DB_ENGINE=django.db.backends.postgresql
```
- Указываем имя базы данных:
```
DB_NAME=postgres 
```
- Указываем логин для подключения к базе данных:
```
POSTGRES_USER=postgres
```
- Указываем пароль для подключения к БД:
```
POSTGRES_PASSWORD=postgres 
```
- Указываем название сервиса/контейнера:
```
DB_HOST=db 
```
- Указываем порт для подключения к БД:
```
DB_PORT=5432 
```
### Запуск проекта в dev-режиме
- Скопировать репозиторий на локальную машину:
```
git clone git@github.com:Jelister203/infra_sp2.git
```
- Перейти в директорию infra:
```
C:/.../infra_sp2/>cd infra
```
- Выполнить команду:
```
docker-compose up -d --build
```