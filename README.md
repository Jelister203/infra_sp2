# Учебный проект infra_sp2
### Описание
Этот проект может многое.
### Технологии
Python 3.7
Django 2.2.19
### Шаблон заполнения env-файла
- Заполните файл .env.template в директории infra/ данными, после чего, выполните команду:
```
cp infra/.env.template infra/.env
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
docker compose up -d --build
```
### Имторт данных из фикстур
- Поместить фикстуру в любой директории проекта, например, api_yamdb
```
...infra_sp2/api_yamdb/fixtures.json
```
- Запустить проект и выполнить команду:
```
docker compose exec web python manage.py loaddata <фикстура>
```
### Автор проекта
- Решетняк Михаил