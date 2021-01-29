import sqlite3
import os
import sys

from typing import List, Tuple, Union


class Address:
    def __init__(self, admin_division_code: str, old_postal_code: str, postal_code: str, prefecture_kana: str,
                 city_kana: str, town_area_kana: str,
                 prefecture_kanji: str, city_kanji: str, town_area_kanji: str, prefecture_eng: str, city_eng: str,
                 town_area_eng: str,
                 multiple_postal_code: int, multiple_address: int, has_chome: int, multiple_town_area: int):
        self.admin_division_code = admin_division_code
        self.old_postal_code = old_postal_code
        self.postal_code = postal_code
        self.prefecture_kana = prefecture_kana
        self.city_kana = city_kana
        self.town_area_kana = town_area_kana
        self.prefecture_kanji = prefecture_kanji
        self.city_kanji = city_kanji
        self.town_area_kanji = town_area_kanji
        self.prefecture_eng = prefecture_eng
        self.city_eng = city_eng
        self.town_area_eng = town_area_eng
        self.multiple_postal_code = bool(multiple_postal_code)
        self.multiple_address = bool(multiple_address)
        self.has_chome = bool(has_chome)
        self.multiple_town_area = bool(multiple_town_area)

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

    def __repr__(self):
        return "<Address: 〒{}-{}, {} {} {}({} {} {})>".format(self.postal_code[:3], self.postal_code[3:],
                                                              self.prefecture_kanji, self.city_kanji,
                                                              self.town_area_kanji, self.prefecture_eng,
                                                              self.city_eng, self.town_area_eng)


class Jusho:
    def __init__(self):
        if os.path.isfile(os.path.join(os.path.dirname(__file__), 'data/address.db')):
            self.conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'data/address.db'))
        elif os.path.exists(os.path.join(sys.prefix, 'data/address.db')):
            self.conn = sqlite3.connect(os.path.join(sys.prefix, 'data/address.db'))
        else:
            raise FileNotFoundError("database file not found")
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

    def cities_from_prefecture(self, prefecture: str, type='kana') -> List[Tuple[str]]:
        assert type in ('kana', 'kanji', 'eng')
        if type == 'kana':
            self.c.execute("SELECT distinct city_kana, city_kanji, city_eng FROM address WHERE prefecture_kana=?",
                           (prefecture,))
        elif type == 'kanji':
            self.c.execute("SELECT distinct city_kana, city_kanji, city_eng FROM address WHERE prefecture_kanji=?",
                           (prefecture,))
        else:
            self.c.execute("SELECT distinct city_kana, city_kanji, city_eng FROM address WHERE prefecture_eng=?",
                           (prefecture,))
        return self.c.fetchall()

    def towns_from_city(self, prefecture: str, city: str, type='kana') -> List[Address]:
        assert type in ('kana', 'kanji', 'eng')
        if type == 'kana':
            self.c.execute("SELECT distinct * FROM address WHERE prefecture_kana=? AND city_kana=?", (prefecture, city))
        elif type == 'kanji':
            self.c.execute("SELECT distinct * FROM address WHERE prefecture_kanji=? AND city_kanji=?",
                           (prefecture, city))
        else:
            self.c.execute("SELECT distinct * FROM address WHERE prefecture_eng=? AND city_eng", (prefecture, city))
        return [Address(*result) for result in self.c.fetchall()]

    def address_from_town(self, prefecture: str, city: str, town: str, type='kana') -> Union[List[Address], List[None]]:
        assert type in ('kana', 'kanji', 'eng')
        if type == 'kana':
            self.c.execute(
                "SELECT distinct * FROM address WHERE prefecture_kana=? AND city_kana=? AND town_area_kana=?",
                (prefecture, city, town))
        elif type == 'kanji':
            self.c.execute(
                "SELECT distinct * FROM address WHERE prefecture_kanji=? AND city_kanji=? AND town_area_kanji=?",
                (prefecture, city, town))
        else:
            self.c.execute("SELECT distinct * FROM address WHERE prefecture_eng=? AND city_eng=? AND town_area_eng=?",
                           (prefecture, city, town))
        result = self.c.fetchone()
        return Address(*result) if result else [None]

    def close(self):
        self.conn.close()

    def __del__(self):
        self.close()
