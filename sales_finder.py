""" This is a simple class that will fetch the cheapest games on sale and its details from the cheapshark api and rawg api.
    1. This will include the game that are on sale
    2. The store that the game belongs to
    3. Savings i.e. discount on the game
    4. The link to the game in the respective store
    5. The banner of the game
    6. The game's rating
    9. The game's description
"""

import requests
import re
import os
from api_locator import APILocator
from game_sales_api import GameSalesAPI
from discord import SelectOption
from game_sales_api import Store

class GameSalesFinder:
    def __init__(self, rawg_api_key):
        self.rawg_api_key = rawg_api_key
        self.cheapshark_base_url = 'https://www.cheapshark.com/api/1.0'
        self.rawg_base_url = 'https://api.rawg.io/api'

    def fetch_sale_games(self, limit, stores, sort_options, **kwargs):
        lst = []
        for store in stores:
            lst.append(Store(
                name=store.label,
                id=store.value,
            ))

        games = APILocator.get_api().fetch_game_sales(limit=limit, stores=lst, sort_by=(sort_options[0] if sort_options else None), **kwargs)

        deals = []
        for game in games:
            try:
                game_details = self._fetch_game_details(game.game_title)
                deal = {
                    'title': game.game_title,
                    'savings': str(int(float(game.percentage_off))) + '%',
                    'store_link': game.store_link,
                    'store_name': game.store_name,
                    'game_cover': game_details['background_image'],
                    'description': GameSalesFinder._remove_special_characters(game_details['description_raw']),
                    'metacritic_rating': game_details['metacritic'],
                    'rating': game_details['ratings'][0]['title'] if game_details['ratings'] else None,
                }
                deals.append(deal)
            except:
                print('Error fetching game details for ' + game.game_title)
                continue

        return deals
    
    def get_stores(self):
        return APILocator.get_api().fetch_game_stores()

    def  _fetch_game_details(self, title: str):
        new_title = GameSalesFinder._remove_non_alphanumeric(title)
        params = {
            'key': self.rawg_api_key,
            'search': new_title,
            'search_precise': 'true',
            'page-size': '1',
        }

        response = requests.get(self.rawg_base_url + '/games', params=params)
        response.raise_for_status()
        
        game_details = dict(response.json())
        if len(game_details['results']) <= 0:
            raise Exception('No game found of title ' + title)
        
        response = requests.get(self.rawg_base_url + '/games/' + game_details['results'][0]['slug'], params={ 'key': self.rawg_api_key })
        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def _remove_non_alphanumeric(string: str) -> str:
        cleaned_string = re.sub(r'[^a-zA-Z0-9\s]', r' ', string)
        return cleaned_string
    
    @staticmethod
    def _remove_special_characters(string: str) -> str:
        cleaned_string = re.sub(r'[@#$%^&*()+=\-\{\}\<\>\[\]/]', r'', string)
        return cleaned_string
    
game_sales = GameSalesFinder(os.getenv('RAWG_API_KEY'))