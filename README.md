# REST API for restaurant menu


## Установка

1. Скачайте репозиторий
```sh
git clone git@github.com:KuzenkovAG/restaurant_menu.git
```
2. Перейдите в папку с проектом
```sh
cd restaurant_menu/
```
3. Создайте .env
```sh
cat .env-example > .env
```


## Запуск тестов postman
#### ВАЖНО
При запуске docker-compose.production.yml, сразу запускается celery и наполняет базу данными из excel.<br>
Если необходимо запустить postman тесты нужно:
1. Остановить контейнера (Если они запускались ранее)
```sh
docker compose -f docker-compose.production.yml stop
```
2. Убедиться что база очищена (если база чистая и кеш чистый, можно переходить к следующему пункту)<br>
Для очистки базы и кеша:
```sh
rm -r data/pg_data/
rm -r data/redis_cache/
```
3. Запустить контейнеры без celery
```sh
docker compose -f docker-compose.postman-tests.yml up --build -d
```
## Запуск приложения
```sh
docker compose -f docker-compose.production.yml up --build -d
```
Приложение - [открыть в браузере](http://127.0.0.1:8000/docs)<br>
Админка Google Sheet - [ссылка](https://docs.google.com/spreadsheets/d/1Fk0z7zcl8A5ugGeoZ-DKi9vB_j9XUQyBUSo2sz3W0DA/edit#gid=0)<br>
## Запуск тестов Pytest
```sh
docker compose -f docker-compose.testing.yml up --build
```


## Задания со звездочкой
#### ДЗ-2
* Реализовать вывод количества подменю и блюд для Меню через один (сложный) ORM запрос.<br>
Запрос для меню - [src/menus/repositories.py: 23-36](https://github.com/KuzenkovAG/restaurant_menu/blob/c363ee75c843fc91eede72ef5863c2975d364a45/src/menus/repositories.py#L25C8-L25C8)<br>
Запрос для подменю- [src/submenus/repositories.py: 25-38](https://github.com/KuzenkovAG/restaurant_menu/blob/c363ee75c843fc91eede72ef5863c2975d364a45/src/submenus/repositories.py#L27)<br>
* Реализовать тестовый сценарий «Проверка кол-ва блюд и подменю в меню» из Postman с помощью pytest<br>
[tests/test_counts.py: 11-76](https://github.com/KuzenkovAG/restaurant_menu/blob/c363ee75c843fc91eede72ef5863c2975d364a45/tests/test_counts.py#L11)<br>
#### ДЗ-3
* Реализовать в тестах аналог Django reverse() для FastAPI<br>
Реализовано во всех тестах, где происходит обращение к url.<br>
Пример: [tests/test_menus.py: 24](https://github.com/KuzenkovAG/restaurant_menu/blob/c363ee75c843fc91eede72ef5863c2975d364a45/tests/test_menus.py#L24C1-L24C1)<br>

#### ДЗ-4
* Обновление меню из google sheets раз в 15 сек.
```python
FROM_GOOGLE_SHEETS = True  # True - из Google sheet, False из файла src/admin/Menu.xlsx
```
[Таблица google sheets](https://docs.google.com/spreadsheets/d/1Fk0z7zcl8A5ugGeoZ-DKi9vB_j9XUQyBUSo2sz3W0DA/edit#gid=0)<br>
Настройка админки - [src/config.py: 34-40](https://github.com/KuzenkovAG/restaurant_menu/blob/c363ee75c843fc91eede72ef5863c2975d364a45/src/config.py#L40)<br>
Проверка условия откуда идет сбор данных - [src/admin/update_db.py: 215](https://github.com/KuzenkovAG/restaurant_menu/blob/c363ee75c843fc91eede72ef5863c2975d364a45/src/admin/update_db.py#L212)<br>
Получение данных из excel - [src/admin/parser.py: 53:..](https://github.com/KuzenkovAG/restaurant_menu/blob/c363ee75c843fc91eede72ef5863c2975d364a45/src/admin/parsers.py#L53)<br>
* Скидка (колонка G в таблице).<br>
Модель - [src/dishes/models.py: 20](https://github.com/KuzenkovAG/restaurant_menu/blob/d7c37b26ed60e9940e88a9ae38347617a535a062/src/dishes/models.py#L20)<br>
Вывод пользователю - [src/dishes/schemas.py: 17:21](https://github.com/KuzenkovAG/restaurant_menu/blob/d7c37b26ed60e9940e88a9ae38347617a535a062/src/dishes/schemas.py#L17)<br>
Получение из админки - [src/admin/parsers.py: 92](https://github.com/KuzenkovAG/restaurant_menu/blob/d7c37b26ed60e9940e88a9ae38347617a535a062/src/admin/parsers.py#L92)<br>

## Install pre-commit hooks (windows)
1. Install venv
```sh
py -3.10 -m venv venv
```
2. Activate it
```sh
source venv/Scripts/activate
```
3. Install package
```sh
pip install pre-commit
```
4. Install pre-commit hooks
```sh
pre-commit install
```
5. Use it.
```sh
pre-commit run --all-files
```

## Usage

Using swagger for auto documentation.
Full available endpoint you can see after starting local server
```url
http://127.0.0.1:8000/docs#/
```

## Endpoints
### Menu operations
- **Get menus**
GET: */api/v1/menus/*
*Response*
```
[
  {
    "title": "string",
    "description": "string",
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "submenus_count": 0,
    "dishs_count": 0
  }
]
```
 - **Get menu**
GET: */api/v1/menus/{menu_id}*
*Response*
```
{
  "title": "string",
  "description": "string",
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "submenus_count": 0,
  "dishs_count": 0
}
```
 - **Create menu**
POST: */api/v1/menus/*
*Request body*
```
{
  "title": "string",
  "description": "string"
}
```
*Response*
```
{
  "title": "string",
  "description": "string",
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```
 - **Update menu**
PATCH: */api/v1/menus/{menu_id}*
*Request body*
```
{
  "title": "string",
  "description": "string"
}
```
*Response*
```
{
  "title": "string",
  "description": "string",
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```
 - **Delete menu**
DELETE: */api/v1/menus/{menu_id}*

### SubMenu operations
- **Get submenus**
GET: */api/v1/menus/{menu_id}/submenus/*
*Response*
```
[
  {
    "title": "string",
    "description": "string",
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "menu_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "dishes_count": 0
  }
]
```
- **Get submenu**
GET: */api/v1/menus/{menu_id}/submenus/{submenu_id}*
*Response*
```
{
  "title": "string",
  "description": "string",
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "menu_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "dishes_count": 0
}
```
- **Create submenu**
POST: */api/v1/menus/{menu_id}/submenus/*
*Request body*
```
{
  "title": "string",
  "description": "string"
}
```
*Response*
```
{
  "title": "string",
  "description": "string",
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "menu_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```
- **Update submenu**
PATCH: */api/v1/menus/{menu_id}/submenus/{submenu_id}*
*Request body*
```
{
  "title": "string",
  "description": "string"
}
```
*Response*
```
{
  "title": "string",
  "description": "string",
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "menu_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "dishes_count": 0
}
```
- **Delete submenu**
DELETE: */api/v1/menus/{menu_id}/submenus/{submenu_id}*

### Dish operations
- **Get dishes**
GET: */api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/*
*Response*
```
[
  {
    "title": "string",
    "description": "string",
    "price": "3.12",
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
  }
]
```
- **Get dish**
GET: */api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}*
*Response*
```
{
  "title": "string",
  "description": "string",
  "price": "3.12",
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```
- **Create dish**
POST: */api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/*
*Request body*
```
{
  "title": "string",
  "description": "string",
  "price": "3.12"
}
```
*Response*
```
{
  "title": "string",
  "description": "string",
  "price": "3.12",
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```
- **Update dish**
PATCH: */api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}*
*Request body*
```
{
  "title": "string",
  "description": "string",
  "price": "3.12"
}
```
*Response*
```
{
  "title": "string",
  "description": "string",
  "price": "3.12",
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```
- **Delete dish**
DELETE: */api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}*
