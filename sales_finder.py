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

class GameSalesFinder:
    def __init__(self, rawg_api_key):
        self.rawg_api_key = rawg_api_key
        self.cheapshark_base_url = 'https://www.cheapshark.com/api/1.0'
        self.rawg_base_url = 'https://api.rawg.io/api'
        self.stores = self._fetch_stores()

    def fetch_sale_games(self, length = None):
        params = {
            'onSale': 'true',
            'pageSize': length if length != None else '60'
        }

        response = requests.get(self.cheapshark_base_url + '/deals', params=params)
        if response.status_code != 200:
            raise Exception('Could not fetch games')
                
        deals = []
        for game in response.json():
            game_details = self._fetch_game_details(game['title'])
            deal = {
                'title': game['title'],
                'store_id': game['storeID'],
                'savings': game['savings'],
                'store_link': 'https://www.cheapshark.com/redirect?dealID=' + game['dealID'],
                'game_cover': game_details['background_image'],
                'description': game_details['description_raw'],
            }
            
            deals.append(deal)

        return deals
    
    def get_stores(self):
        return self.stores

    def get_store_name(self, id):
        for store in self.stores:
            if store['storeID'] == id:
                return store['storeName']
    
    def _fetch_stores(self):
        params = {
            'key': self.rawg_api_key,
        }
        response = requests.get(self.cheapshark_base_url + '/stores', params=params)
        if response.status_code != 200:
            raise Exception('Could not fetch stores')
        return response.json()

    def _fetch_game_details(self, title: str):
        new_title = GameSalesFinder._remove_non_alphanumeric(title)
        params = {
            'key': self.rawg_api_key,
            'search': new_title,
            'search_precise': 'true',
            'page-size': '1',
        }

        response = requests.get(self.rawg_base_url + '/games', params=params)
        if response.status_code != 200:
            raise Exception('Could not fetch game details')
        
        game_details = dict(response.json())
        if len(game_details) < 0:
            raise Exception('No game found of title ' + title)
        
        response = requests.get(self.rawg_base_url + '/games/' + game_details['results'][0]['slug'], params={ 'key': self.rawg_api_key })
        return response.json()
    
    @staticmethod
    def _remove_non_alphanumeric(string: str) -> str:
        cleaned_string = re.sub(r'[^a-zA-Z0-9\s]', r' ', string)
        return cleaned_string
    
game_sales = GameSalesFinder(os.getenv('RAWG_API_KEY'))