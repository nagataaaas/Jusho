from dataclasses import dataclass

TABLE_COUNT = 3


def id_to_table_type(id_: int) -> str:
    tables = ("prefectures", "cities", "addresses")
    return tables[id_ % TABLE_COUNT]


@dataclass(frozen=True)
class Prefecture:
    id: int  # mod TABLE_COUNT = 0
    kanji: str
    kana: str
    eng: str

    @property
    def to_sql(self):
        return f"{self.id}, '{self.kanji}', '{self.kana}', '{self.eng}'"


@dataclass(frozen=True)
class City:
    id: int  # mod TABLE_COUNT = 1

    prefecture: Prefecture
    kanji: str
    kana: str
    eng: str

    @property
    def concat_kanji(self) -> str:
        return f"{self.prefecture.kanji}　{self.kanji}"

    @property
    def concat_kana(self) -> str:
        return f"{self.prefecture.kana}　{self.kana}"

    @property
    def concat_eng(self) -> str:
        return f"{self.eng}, {self.prefecture.eng.title()}".title()


@dataclass(frozen=True)
class Address:
    id: int  # mod TABLE_COUNT = 2

    city: City

    admin_division_code: str
    old_zip_code: str
    zip_code: str

    kanji: str
    kana: str
    eng: str

    multiple_zip_code: bool
    multiple_address: bool
    has_chome: bool
    multiple_town_area: bool

    @property
    def concat_kanji(self) -> str:
        return f"{self.city.concat_kanji}　{self.kanji}"

    @property
    def concat_kana(self) -> str:
        return f"{self.city.concat_kana}　{self.kana}"

    @property
    def concat_eng(self) -> str:
        return f"{self.eng}, {self.city.concat_eng}".title()

    @property
    def prefecture(self) -> Prefecture:
        return self.city.prefecture

    @property
    def hyphen_zip(self):
        return "{}-{}".format(self.zip_code[:3], self.zip_code[3:])

    def __str__(self):
        if self.kanji == "以下に掲載がない場合":
            return "〒{}-{}, {} {}({} {})".format(
                self.zip_code[:3],
                self.zip_code[3:],
                self.prefecture.kanji,
                self.city.kanji,
                self.prefecture.eng,
                self.city.eng,
            )
        return "〒{}-{}, {} {} {}({} {} {})".format(
            self.zip_code[:3],
            self.zip_code[3:],
            self.prefecture.kanji,
            self.city.kanji,
            self.kanji,
            self.prefecture.eng,
            self.city.eng,
            self.eng,
        )
