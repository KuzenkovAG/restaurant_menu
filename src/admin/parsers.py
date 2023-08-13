import abc

import pandas

MENU_ID_COL = 0
MENU_TITLE_COL = 1
MENU_DESC_COL = 2

SUB_ID_COL = 1
SUB_TITLE_COL = 2
SUB_DESC_COL = 3

DISH_ID_COL = 2
DISH_TITLE_COL = 3
DISH_DESC_COL = 4
DISH_PRICE_COL = 5


class BaseParser(abc.ABC):
    """Base parser."""
    @abc.abstractmethod
    async def parse(self) -> dict[str, dict[str, dict]]:
        """
        Parse data to special structure for easy compare.
        Return:
        {
            'menus': {
                '13d81e02-3911-11ee-be56-0242ac120003': {
                    'field_name': 'field_value'
                    ...
                },
                ...
            }
            'submenus': {
                '13d81e02-3911-11ee-be56-0242ac120003': {
                    'field_name': 'field_value'
                    ...
                },
                ...
            }
            'dishes': {
                '13d81e02-3911-11ee-be56-0242ac120003': {
                    'field_name': 'field_value'
                    ...
                },
                ...
            }
        }
        """
        ...


class ExcelParser(BaseParser):
    """Parse admin data from excel."""

    def __init__(self, source: str):
        self.source = source

    async def parse(self) -> dict[str, dict[str, dict]]:
        """Do parse."""
        excel = pandas.read_excel(self.source, index_col=None, header=None)
        data: dict = {
            'menus': {},
            'submenus': {},
            'dishes': {},
        }

        for _, row in excel.iterrows():
            if not pandas.isnull(row[MENU_ID_COL]):
                menu_id = row[MENU_ID_COL]
                data['menus'][menu_id] = {
                    'id': menu_id,
                    'title': row[MENU_TITLE_COL],
                    'description': row[MENU_DESC_COL],
                }
            elif not pandas.isnull(row[SUB_ID_COL]):
                submenu_id = row[SUB_ID_COL]
                data['submenus'][submenu_id] = {
                    'id': submenu_id,
                    'title': row[SUB_TITLE_COL],
                    'description': row[SUB_DESC_COL],
                    'menu_id': menu_id,
                }
            elif not pandas.isnull(row[DISH_ID_COL]):
                dish_id = row[DISH_ID_COL]
                data['dishes'][dish_id] = {
                    'id': dish_id,
                    'title': row[DISH_TITLE_COL],
                    'description': row[DISH_DESC_COL],
                    'price': row[DISH_PRICE_COL],
                    'menu_id': menu_id,
                    'submenu_id': submenu_id,
                }
        return data
