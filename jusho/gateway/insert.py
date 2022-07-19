from sqlite3 import Cursor

from ..models import Prefecture, City, Address

CREATE_TABLES = """
CREATE TABLE prefectures (
    id integer primary key,
    kanji text,
    kana text,
    eng text
);

CREATE TABLE cities (
    id integer primary key,
    prefecture_id integer references prefectures(id),
    kanji text,
    kana text,
    eng text
);
create index prefecture_id_index on cities(prefecture_id);

CREATE TABLE addresses (
    id integer primary key,
    city_id integer references cities(id),
    admin_division_code text,
    old_zip_code text,
    zip_code text,
    kanji text,
    kana text,
    eng text,
    multiple_zip_code integer,
    multiple_address integer,
    has_chome integer,
    multiple_town_area integer
);
create index city_id_index on addresses(city_id);
create index zip_code_index on addresses(zip_code);
"""


def insert_prefecture(cursor: Cursor, prefecture: Prefecture):
    cursor.execute(
        "INSERT INTO prefectures VALUES (?, ?, ?, ?)",
        (prefecture.id, prefecture.kanji, prefecture.kana, prefecture.eng)
    )


def insert_city(cursor: Cursor, city: City):
    cursor.execute(
        "INSERT INTO cities VALUES (?, ?, ?, ?, ?)",
        (city.id, city.prefecture.id, city.kanji, city.kana, city.eng)
    )


def insert_address(cursor: Cursor, address: Address):
    cursor.execute(
        "INSERT INTO addresses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (address.id, address.city.id, address.admin_division_code, address.old_zip_code, address.zip_code,
         address.kanji, address.kana, address.eng, address.multiple_zip_code, address.multiple_address,
         address.has_chome, address.multiple_town_area)
    )
