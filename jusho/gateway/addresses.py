from dataclasses import replace
from sqlite3 import Cursor
from typing import List, Optional

from .utils import data_to_address
from ..models import Prefecture, City, Address


def fetch_address_by_zip_code(cursor: Cursor, zip_code: str) -> List[Address]:
    cursor.execute(f"SELECT p.*, c.*, a.* FROM addresses AS a "
                   f"JOIN cities AS c ON c.id = a.city_id "
                   f"JOIN prefectures AS p ON p.id = c.prefecture_id "
                   f"WHERE a.zip_code=?", (zip_code,))
    data = cursor.fetchall()

    return [data_to_address(v) for v in data]


def fetch_addresses_from_city(cursor: Cursor, city: City) -> List[Address]:
    cursor.execute(f"SELECT * FROM addresses "
                   f"WHERE city_id=?", (city.id,))
    data = cursor.fetchall()
    addresses = []
    for v in data:
        addresses.append(replace(Address(*v), city=city))

    return addresses


def fetch_address_by_id(cursor: Cursor, id_: int) -> Optional[Address]:
    cursor.execute((f"SELECT p.*, c.*, a.* FROM addresses AS a "
                    f"JOIN cities AS c ON c.id = a.city_id "
                    f"JOIN prefectures AS p ON p.id = c.prefecture_id "
                    f"WHERE a.id=?"), (id_,))
    data = cursor.fetchone()
    return data_to_address(data) if data else None


def search_addresses(cursor: Cursor, query: str, prefecture: Prefecture, city: City, type_: str) -> List[Address]:
    query = [f"SELECT p.*, c.*, a.* FROM addresses AS a "
             f"JOIN cities AS c ON c.id = a.city_id "
             f"JOIN prefectures AS p ON p.id = c.prefecture_id "
             f"WHERE a.{type_} LIKE '%{query}%'", []]
    if prefecture:
        query[0] += ' AND p.id = ?'
        query[1].append(prefecture.id)
    if city:
        query[0] += ' AND c.id = ?'
        query[1].append(city.id)
    cursor.execute(*query)
    data = cursor.fetchall()

    return [data_to_address(v) for v in data]


__all__ = [
    'fetch_address_by_zip_code',
    'fetch_addresses_from_city',
    'fetch_address_by_id',
    'search_addresses',
]
