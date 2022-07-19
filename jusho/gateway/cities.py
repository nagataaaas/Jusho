from sqlite3 import Cursor
from typing import List, Optional

from .utils import data_to_city
from ..models import Prefecture, City
from dataclasses import replace


def fetch_cities_from_prefecture(cursor: Cursor, prefecture: Prefecture) -> List[City]:
    cursor.execute(f"SELECT * FROM cities WHERE prefecture_id=?", (prefecture.id,))
    data = cursor.fetchall()
    cities = []
    for v in data:
        cities.append(replace(City(*v), prefecture=prefecture))

    return cities


def fetch_city_by_id(cursor: Cursor, id_: int) -> Optional[City]:
    cursor.execute((f"SELECT p.*, c.* FROM cities AS c "
                    f"JOIN prefectures AS p ON p.id = c.prefecture_id "
                    f"WHERE c.id=?"), (id_,))
    data = cursor.fetchone()
    return data_to_city(data) if data else None


def search_cities(cursor: Cursor, query: str, prefecture: Prefecture, type_: str) -> List[City]:
    query = [f"SELECT p.*, c.* FROM cities AS c "
             f"JOIN prefectures AS p ON p.id = c.prefecture_id "
             f"WHERE c.{type_} LIKE '%{query}%'", []]
    if prefecture:
        query[0] += ' AND p.id = ?'
        query[1].append(prefecture.id)

    cursor.execute(*query)
    data = cursor.fetchall()

    return [data_to_city(v) for v in data]
