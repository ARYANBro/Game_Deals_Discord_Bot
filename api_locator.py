from game_sales_api import GameSalesAPI

from cheapsharkapi import CheapSharkAPI

class APILocator:

    sales_api = None

    @classmethod
    def provide_api(cls, api):
        cls.sales_api = api

    @classmethod
    def get_api(cls) -> type[GameSalesAPI]:
        return CheapSharkAPI