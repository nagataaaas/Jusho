from collections import Counter

import pytest

from jusho import Jusho, Prefecture, City, Address


class TestJusho:
    """
    tests class of jusho
    """

    postman = Jusho()

    def test_by_zip_code(self):
        zip_codes = ["1600021", "160-0021", "160 0021", "〒160-0021"]
        for code in zip_codes:
            addresses = self.postman.by_zip_code(code)
            assert 1 == len(addresses)
            address = addresses[0]
            assert "160-0021" == address.hyphen_zip
            assert "歌舞伎町" == address.kanji
            assert "新宿区" == address.city.kanji
            assert "東京都" == address.prefecture.kanji
            assert "東京都　新宿区　歌舞伎町" == address.concat_kanji
            assert "トウキョウト　シンジュクク　カブキチョウ" == address.concat_kana
            assert "Kabukicho, Shinjuku Ku, Tokyo To" == address.concat_eng

    def test_prefectures(self):
        prefectures = self.postman.prefectures
        assert 47 == len(prefectures)
        lasts = Counter([p.kanji[-1] for p in prefectures])
        assert 1 == lasts["都"]
        assert 2 == lasts["府"]
        assert 1 == lasts["道"]

    def test_search_prefectures(self):
        prefectures = self.postman.search_prefectures("東京", "kanji")
        assert 1 == len(prefectures)
        assert "東京都" == prefectures[0].kanji

        prefectures = self.postman.search_prefectures("トウキョウト", "kana")
        assert 1 == len(prefectures)
        assert "トウキョウト" == prefectures[0].kana

        prefectures = self.postman.search_prefectures("tokyo", "eng")
        assert 1 == len(prefectures)
        assert "tokyo to" == prefectures[0].eng.lower()

    def test_cities(self):
        pref = self.postman.search_prefectures("東京", "kanji")[0]
        cities = self.postman.cities(pref)
        assert 62 == len(cities)
        assert pref == cities[0].prefecture

    def test_search_cities(self):
        tokyo = self.postman.search_prefectures("東京", "kanji")[0]
        osaka = self.postman.search_prefectures("大阪", "kanji")[0]
        cities = self.postman.search_cities("大阪市都島区")
        assert 1 == len(cities)
        assert osaka == cities[0].prefecture

        cities = self.postman.search_cities("大阪市都島区", prefecture=tokyo)
        assert 0 == len(cities)

    def test_addresses(self):
        tokyo = self.postman.search_prefectures("東京", "kanji")[0]
        cities = self.postman.search_cities("新宿", prefecture=tokyo)
        assert 1 == len(cities)
        city = cities[0]

        addresses = self.postman.addresses(city)
        assert 696 == len(addresses)
        assert city == addresses[0].city

    def test_search_addresses(self):
        tokyo = self.postman.search_prefectures("東京", "kanji")[0]
        osaka = self.postman.search_prefectures("大阪", "kanji")[0]
        cities = self.postman.search_cities("新宿", prefecture=tokyo)
        assert 1 == len(cities)
        city = cities[0]

        addresses = self.postman.search_addresses("歌舞伎町", city=city)
        assert 1 == len(addresses)
        address = addresses[0]
        assert "歌舞伎町" == address.kanji
        assert "新宿区" == address.city.kanji
        assert "東京都" == address.prefecture.kanji
        assert "東京都　新宿区　歌舞伎町" == address.concat_kanji
        assert "トウキョウト　シンジュクク　カブキチョウ" == address.concat_kana
        assert "Kabukicho, Shinjuku Ku, Tokyo To" == address.concat_eng

        with pytest.raises(ValueError):
            self.postman.search_addresses("歌舞伎町", city=city, prefecture=osaka)
        addresses = self.postman.search_addresses("歌舞伎町", prefecture=osaka)
        assert 0 == len(addresses)

    def test_get_by_id(self):
        assert isinstance(self.postman.fetch_by_id(0), Prefecture)
        assert isinstance(self.postman.fetch_by_id(1), City)
        assert isinstance(self.postman.fetch_by_id(2), Address)
        assert isinstance(self.postman.fetch_by_id(3), Prefecture)

    def test_prefecture_by_id(self):
        prefecture = self.postman.prefecture_by_id(0)
        assert isinstance(prefecture, Prefecture)

        with pytest.warns(RuntimeWarning):
            self.postman.prefecture_by_id(1)

    def test_city_by_id(self):
        city = self.postman.city_by_id(1)
        assert isinstance(city, City)

        with pytest.warns(RuntimeWarning):
            self.postman.city_by_id(2)

    def test_address_by_id(self):
        address = self.postman.address_by_id(2)
        assert isinstance(address, Address)

        with pytest.warns(RuntimeWarning):
            self.postman.address_by_id(3)


if __name__ == "__main__":
    pytest.main()
