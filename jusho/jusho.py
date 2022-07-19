import os
import re
import sqlite3
import sys
import warnings
from typing import List, Union

from jusho import gateway
from .models import Address, Prefecture, City, id_to_table_type


def get_database_path() -> str:
    if os.path.isfile(os.path.join(os.path.dirname(__file__), 'data/address.db')):
        return os.path.join(os.path.dirname(__file__), 'data/address.db')
    elif os.path.isfile(os.path.join(sys.prefix, 'data/address.db')):
        return os.path.join(sys.prefix, 'data/address.db')
    elif os.path.isfile(os.path.join(os.path.dirname(__file__).rsplit('lib', 1)[0], 'data/address.db')):
        return os.path.join(os.path.dirname(__file__).rsplit('lib', 1)[0], 'data/address.db')
    else:
        raise FileNotFoundError("database file not found")


class Jusho:
    def __init__(self, database_path=None):
        path = database_path or get_database_path()
        if not os.path.exists(path):
            raise FileNotFoundError("database file not found. \n"
                                    "Consider to create a database file with jusho.create_database()")
        self.conn = sqlite3.connect(database_path or get_database_path())
        self.cursor = self.conn.cursor()
        self.c = self.cursor

    def by_zip_code(self, zip_code: str) -> List[Address]:
        zip_code = ''.join(re.findall(r'\d+', zip_code))
        return gateway.addresses.fetch_address_by_zip_code(self.cursor, zip_code)

    def fetch_by_id(self, id_: int) -> Union[Prefecture, City, Address]:
        table = id_to_table_type(id_)
        if table == 'prefectures':
            return self.prefecture_by_id(id_)
        elif table == 'cities':
            return self.city_by_id(id_)
        elif table == 'addresses':
            return self.address_by_id(id_)
        else:
            raise ValueError(f"id_: {id_} does not seem to be a valid id")

    # #-#-#-#-#-#-#-#-# PREFECTURES #-#-#-#-#-#-#-#-# #
    def search_prefectures(self, query: str, type_='kanji') -> List[Prefecture]:
        return gateway.prefectures.search_prefectures(self.cursor, query, type_)

    @property
    def prefectures(self) -> List[Prefecture]:
        return gateway.prefectures.fetch_prefectures(self.cursor)

    def prefecture_by_id(self, id_: int) -> Prefecture:
        table = id_to_table_type(id_)
        if table != 'prefectures':
            warnings.warn(f"id_: {id_} does not seem to be a prefecture id. rather, it's a {table} id", RuntimeWarning)
        return gateway.prefectures.fetch_prefecture_by_id(self.cursor, id_)

    # #-#-#-#-#-#-#-#-# CITIES #-#-#-#-#-#-#-#-# #
    def cities(self, prefecture: Prefecture) -> List[City]:
        return gateway.cities.fetch_cities_from_prefecture(self.cursor, prefecture)

    def search_cities(self, query: str, prefecture: Prefecture = None, type_='kanji') -> List[City]:
        """
        search cities from query
        if prefecture is specified, search cities from prefecture
        """
        if type_ not in ('kanji', 'kana', 'eng'):
            raise ValueError("type must be one of 'kanji', 'kana', 'eng'")

        return gateway.cities.search_cities(self.cursor, query, prefecture, type_)

    def city_by_id(self, id_: int) -> City:
        table = id_to_table_type(id_)
        if table != 'cities':
            warnings.warn(f"id_: {id_} does not seem to be a city id. rather, it's a {table} id", RuntimeWarning)
        return gateway.cities.fetch_city_by_id(self.cursor, id_)

    # #-#-#-#-#-#-#-#-# ADDRESSES #-#-#-#-#-#-#-#-# #
    def addresses(self, city: City) -> List[Address]:
        return gateway.addresses.fetch_addresses_from_city(self.cursor, city)

    def search_addresses(self, query: str,
                         prefecture: Prefecture = None, city: City = None, type_='kanji') -> List[Address]:
        """
        search addresses from query
        if prefecture is specified, search addresses from prefecture
        if city is specified, search addresses from city
        You can specify prefecture and city at the same time. But city must be a part of prefecture, and it's meaningless.
        """
        if type_ not in ('kanji', 'kana', 'eng'):
            raise ValueError("type must be one of 'kanji', 'kana', 'eng'")
        if prefecture and city:
            if city.prefecture != prefecture:
                raise ValueError("city must be a part of prefecture")

        return gateway.addresses.search_addresses(self.cursor, query, prefecture, city, type_)

    def address_by_id(self, id_: int) -> Address:
        table = id_to_table_type(id_)
        if table != 'addresses':
            warnings.warn(f"id_: {id_} does not seem to be a address id. rather, it's a {table} id", RuntimeWarning)
        return gateway.addresses.fetch_address_by_id(self.cursor, id_)

    def close(self):
        self.conn.close()

    def __del__(self):
        self.close()
