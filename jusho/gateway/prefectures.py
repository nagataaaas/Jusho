from sqlite3 import Cursor
from typing import List, Optional

from ..models import Prefecture


def fetch_prefectures(cursor: Cursor) -> List[Prefecture]:
    cursor.execute("SELECT * FROM prefectures")
    return [Prefecture(*v) for v in cursor.fetchall()]


def fetch_prefecture_by_id(cursor: Cursor, id_: int) -> Optional[Prefecture]:
    cursor.execute("SELECT * FROM prefectures WHERE id=?", (id_,))
    data = cursor.fetchone()
    return Prefecture(*data) if data else None


def search_prefectures(cursor: Cursor, query: str, type_: str) -> List[Prefecture]:
    cursor.execute(f"SELECT * FROM prefectures WHERE {type_} LIKE '%{query}%'")
    return [Prefecture(*v) for v in cursor.fetchall()]
