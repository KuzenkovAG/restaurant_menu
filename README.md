# REST API for restaurant menu


## Installation

1. Clone repository
```sh
git clone git@github.com:KuzenkovAG/restaurant_menu.git
```
2. Go to folder
```sh
cd restaurant_menu/
```
3. Create .env
```sh
cat .env-example > .env
```
4. Run app (after )
```sh
docker compose -f docker-compose.production.yml up --build -d
```
### Test run
1. Create .env
```sh
cat .env-example > .env
```
2. Run command
```sh
docker compose -f docker-compose.testing.yml up --build
```

#### Задания со звездочкой
## ДЗ-2
* Реализовать вывод количества подменю и блюд для Меню через один (сложный) ORM запрос.
src/menus/repositories.py: 23-36
src/submenus/repositories.py: 25-38
* Реализовать тестовый сценарий «Проверка кол-ва блюд и подменю в меню» из Postman с помощью pytest
tests/test_counts.py: 11-76
## ДЗ-3
* Реализовать в тестах аналог Django reverse() для FastAPI
tests/test_menus.py: 24, 43, 71 .... (везде где происходит обращение к url)
## ДЗ-4
* Обновление меню из google sheets раз в 15 сек.
google sheets - [ссылка]
src/config.py: 17-21
FROM_GOOGLE_SHEETS = False  # False из файла src/admin/Menu.xlsx, True - из Google sheet
src/admin/update_db.py: 215

#### Install pre-commit hooks (windows)
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


[ссылка]: <https://docs.google.com/spreadsheets/d/1Fk0z7zcl8A5ugGeoZ-DKi9vB_j9XUQyBUSo2sz3W0DA/edit#gid=0>
