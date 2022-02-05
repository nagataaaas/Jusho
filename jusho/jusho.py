import sqlite3
import os
import sys

from typing import List, Tuple, Union
from dataclasses import dataclass


def get_database_path() -> str:
    if os.path.isfile(os.path.join(os.path.dirname(__file__), 'data/address.db')):
        return os.path.join(os.path.dirname(__file__), 'data/address.db')
    elif os.path.isfile(os.path.join(sys.prefix, 'data/address.db')):
        return os.path.join(sys.prefix, 'data/address.db')
    elif os.path.isfile(os.path.join(os.path.dirname(__file__).rsplit('lib', 1)[0], 'data/address.db')):
        return os.path.join(os.path.dirname(__file__).rsplit('lib', 1)[0], 'data/address.db')
    else:
        raise FileNotFoundError("database file not found")


@dataclass(frozen=True)
class Address:
    admin_division_code: str
    old_postal_code: str
    postal_code: str
    prefecture_kana: str
    city_kana: str
    town_area_kana: str
    prefecture_kanji: str
    city_kanji: str
    town_area_kanji: str
    prefecture_eng: str
    city_eng: str
    town_area_eng: str
    multiple_postal_code: bool
    multiple_address: bool
    has_chome: bool
    multiple_town_area: bool

    @property
    def to_sql(self):
        return f"'{self.admin_division_code}', '{self.old_postal_code}', '{self.postal_code}', " \
               f"'{self.prefecture_kana}', '{self.city_kana}', '{self.town_area_kana}', '{self.prefecture_kanji}', " \
               f"'{self.city_kanji}', '{self.town_area_kanji}', '{self.prefecture_eng}', '{self.city_eng}', " \
               f"'{self.town_area_eng}', {self.multiple_postal_code}, {self.multiple_address}, " \
               f"{self.has_chome}, {self.multiple_town_area}"

    @property
    def hyphen_postal(self):
        return "{}-{}".format(self.postal_code[:3], self.postal_code[3:])

    def __str__(self):
        if self.town_area_kanji == '以下に掲載がない場合':
            return "〒{}-{}, {} {}({} {})".format(self.postal_code[:3], self.postal_code[3:],
                                                 self.prefecture_kanji, self.city_kanji,
                                                 self.prefecture_eng, self.city_eng)
        return "〒{}-{}, {} {} {}({} {} {})".format(self.postal_code[:3], self.postal_code[3:],
                                                   self.prefecture_kanji, self.city_kanji,
                                                   self.town_area_kanji, self.prefecture_eng,
                                                   self.city_eng, self.town_area_eng)


class Jusho:
    def __init__(self):
        self.conn = sqlite3.connect(get_database_path())
        self.c = self.conn.cursor()

    def from_postal_code(self, postal_code: str) -> Union[Address, None]:
        postal_code = str(postal_code).replace('〒', '').replace('-', '').strip()
        self.c.execute("SELECT * FROM address WHERE postal_code=?", (postal_code,))
        result = self.c.fetchone()
        return Address(*result) if result else None

    @property
    def prefectures(self) -> List[Tuple[str]]:
        self.c.execute("SELECT distinct prefecture_kana, prefecture_kanji, prefecture_eng FROM address")
        return self.c.fetchall()

    def cities_from_prefecture(self, prefecture: str, type_='kana') -> List[Tuple[str]]:
        if type_ not in ('kana', 'kanji', 'eng'):
            raise ValueError("type must be one of 'kana', 'kanji', 'eng'")

        self.c.execute(f"SELECT distinct city_kana, city_kanji, city_eng FROM address WHERE prefecture_{type_}=?",
                       (prefecture,))
        return self.c.fetchall()

    def towns_from_city(self, prefecture: str, city: str, type_='kana') -> List[Address]:
        if type_ not in ('kana', 'kanji', 'eng'):
            raise ValueError("type must be one of 'kana', 'kanji', 'eng'")

        self.c.execute(f"SELECT distinct * FROM address WHERE prefecture_{type_}=? AND city_{type_}=?",
                       (prefecture, city))
        return [Address(*result) for result in self.c.fetchall()]

    def address_from_town(self, prefecture: str, city: str, town: str, type_='kana') -> Union[
        List[Address], List[None]]:
        if type_ not in ('kana', 'kanji', 'eng'):
            raise ValueError("type must be one of 'kana', 'kanji', 'eng'")

        self.c.execute(
            f"SELECT distinct * FROM address WHERE prefecture_{type_}=? AND city_{type_}=? AND town_area_{type_}=?",
            (prefecture, city, town))
        result = self.c.fetchone()
        return Address(*result) if result else [None]

    def close(self):
        self.conn.close()

    def __del__(self):
        self.close()
