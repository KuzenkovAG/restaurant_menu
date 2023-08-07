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
4. Run app
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
