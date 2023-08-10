from game_sales_api import GameSalesAPI, SaleDetails, Store
import requests
import os
from enum import Enum


class ITAD_SortOptions(Enum):
    """Enum for sort by properties for the ITAD API"""
    DATE_RECENT = 'time:asc'
    DATE_OLDEST = 'time:desc'
    PRICE_CHEAPEST = 'price:asc'
    PRICE_MOST_EXPENSIVE = 'price:desc'


class ITAD_API(GameSalesAPI):
    """Implementation nof the GamesSalesApi interface for the ITAD API"""

    _base_url = 'https://api.isthereanydeal.com/v01'
    _api_key = os.getenv('ISTHEREANYDEAL_API_KEY')

    @staticmethod
    def fetch_game_sales(limit=1, stores: list[Store] = [], sort_by: ITAD_SortOptions = ITAD_SortOptions.PRICE_MOST_EXPENSIVE) -> list[SaleDetails]:
        params = {
            'key': ITAD_API._api_key,
            'limit': str(limit),
            'sort': sort_by.value,
        }

        # If stores is not None, we add it to the params
        if stores is not None:
            store_str = str()
            for store in stores:
                store_str += str(store.id) + ','
            store_str = store_str.rstrip(',')
            params['shops'] = str(store_str)

        response = requests.get(ITAD_API._base_url + '/deals/list/', params=params)
        response.raise_for_status()

        ret = []

        for game in response.json()['data']['list']:
            ret.append(SaleDetails(
                game_title=game['title'],
                percentage_off=game['price_cut'],
                store_name=game['shop']['name'],
                store_link=game['urls']['buy']
            ))

        return ret

    @staticmethod
    def fetch_game_stores() -> list[Store]:
        response = requests.get(ITAD_API._base_url + '/web/stores/all/')
        response.raise_for_status()

        stores = []
        for store in response.json()['data']:
            stores.append(Store(
                name=store['title'],
                id=store['id']
            ))

        return stores

    @staticmethod
    def fetch_game_info(id):
        params = {
            'key': ITAD_API._api_key,
            'plains': id
        }

        response = requests.get(ITAD_API._base_url + '/game/info/', params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_sort_options():
        return ITAD_SortOptions