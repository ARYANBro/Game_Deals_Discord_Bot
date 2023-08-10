"""Abstraction for sales api

    Does three things
    1. fetchs game sales
        - allows to limit number of games to fetch
        - allows to filter by game stores
        - sort by differnt properties
    
    2. fetchs game stores
    3. game sales details
        - game title
        - percentage off
        - store name
        - store link

"""

from abc import ABCMeta, abstractmethod
from enum import Enum

class SaleDetails:
    """Class for sale details"""

    def __init__(self, game_title, percentage_off, store_name, store_link):
        self.game_title = game_title
        self.percentage_off = percentage_off
        self.store_name = store_name
        self.store_link = store_link

class Store:
    """Class identifing stores name and id"""

    def __init__(self, name, id) -> None:
        self.name = name
        self.id = id

class GameSalesAPI(metaclass=ABCMeta):
    """Abstract class for sales api"""

    @staticmethod
    @abstractmethod
    def fetch_game_sales(limit:int=10, stores:list[Store]=[], sort_by=None, **kwargs) -> list[SaleDetails]:
        """Fetches game sales"""

    @staticmethod
    @abstractmethod
    def fetch_game_stores() -> list[Store]:
        """Fetches game stores.
        Raises :class:`HTTPError`, if one occurred.
        """

    @staticmethod
    @abstractmethod
    def get_sort_options() -> type[Enum]:
        """Returns the enum, for sort options, could be specific to the API in use"""

    @staticmethod
    @abstractmethod
    def get_bool_parameters() -> dict[str, str]:
        """Returns boolean parameters for the API: display name and internal name"""