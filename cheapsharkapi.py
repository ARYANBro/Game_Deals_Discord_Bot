from game_sales_api import GameSalesAPI, SaleDetails, Store
import requests
from enum import Enum


class CheapShark_SortOptions(Enum):
    DEAL_RATING = 'Deal Rating'
    METACRITIC = 'Metacritic'
    REVIEWS = 'Reviews'
    RELEASE = 'Release'
    RECENT = 'Recent'
    PRICE = 'Price'
    TITLE = 'Title'
    SAVINGS = 'Savings'
    STORE = 'Store'


class CheapSharkAPI(GameSalesAPI):
    """Implementation of the GamesSalesAPI interface for the CheapShark API."""

    _base_url = "https://www.cheapshark.com/api/1.0/"

    @staticmethod
    def fetch_game_sales(limit, stores:list[Store]=[], sort_by = CheapShark_SortOptions.DEAL_RATING, **kwargs) -> list[SaleDetails]:
        params = {
            'pageSize': str(limit),
            'sortBy': str(sort_by),
        }

        if stores:
            store_str = str()
            for store in stores:
                store_str += str(store.id) + ','
            store_str = store_str.rstrip(',')
            params['storeID'] = store_str

        if len(kwargs) > 0:
            for key, value in kwargs.items():
                params[key] = value

        response = requests.get(CheapSharkAPI._base_url + 'deals', params=params)
        response.raise_for_status()

        if len(response.json()) <= 0:
            raise Exception("Couldn't fetch game sales")
        
        ret = []
        for game in response.json():
            ret.append(SaleDetails(
                game_title=game['title'],
                percentage_off=game['savings'],
                store_name=CheapSharkAPI._get_store_name(game['storeID']),
                store_link=CheapSharkAPI._construct_store_link(game['dealID'])
            ))

        return ret

    @staticmethod
    def fetch_game_stores() -> list[Store]:
        response = requests.get(CheapSharkAPI._base_url + 'stores')
        response.raise_for_status()

        ret = []
        for store in response.json():
            ret.append(Store(
                name=store['storeName'],
                id=store['storeID'],
            ))

        return ret
    
    @staticmethod
    def get_sort_options():
        return CheapShark_SortOptions
    
    @staticmethod
    def get_bool_parameters() -> dict[str, str]:
        return { 
            'On Sale': 'onSale',
            'Steamworks': 'steamworks',
            'Only AAA' : 'AAA',
        }
    
    @staticmethod
    def _get_store_name(store_id: int) -> str:
        store_name = filter(lambda store: store.id == store_id, CheapSharkAPI.fetch_game_stores())
        store_name = list(store_name)

        if len(store_name) > 1:
            raise Exception("Multiple stores with the same ID")

        if len(store_name) == 0:
            raise Exception("Store not found")        
        
        return store_name[0].name

    @staticmethod
    def _construct_store_link(deal_id: int) -> str:
        return f'https://www.cheapshark.com/redirect?dealID={deal_id}'
