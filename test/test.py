import unittest
from collections import Counter

from jusho import Jusho


class TestJusho(unittest.TestCase):
    """
    test class of jusho
    """
    postman = Jusho()

    def test_by_zip_code(self):
        zip_codes = ['1600021', '160-0021', '160 0021', '〒160-0021']
        for code in zip_codes:
            addresses = self.postman.by_zip_code(code)
            self.assertEqual(1, len(addresses))
            address = addresses[0]
            self.assertEqual('160-0021', address.hyphen_zip)
            self.assertEqual('歌舞伎町', address.kanji)
            self.assertEqual('新宿区', address.city.kanji)
            self.assertEqual('東京都', address.prefecture.kanji)
            self.assertEqual('東京都　新宿区　歌舞伎町', address.concat_kanji)
            self.assertEqual('トウキョウト　シンジュクク　カブキチョウ', address.concat_kana)
            self.assertEqual('Kabukicho, Shinjuku Ku, Tokyo To', address.concat_eng)

    def test_prefectures(self):
        prefectures = self.postman.prefectures
        self.assertEqual(47, len(prefectures))
        lasts = Counter([p.kanji[-1] for p in prefectures])
        self.assertEqual(1, lasts['都'])
        self.assertEqual(2, lasts['府'])
        self.assertEqual(1, lasts['道'])

    def test_search_prefectures(self):
        prefectures = self.postman.search_prefectures('東京', 'kanji')
        self.assertEqual(1, len(prefectures))
        self.assertEqual('東京都', prefectures[0].kanji)

        prefectures = self.postman.search_prefectures('トウキョウト', 'kana')
        self.assertEqual(1, len(prefectures))
        self.assertEqual('トウキョウト', prefectures[0].kana)

        prefectures = self.postman.search_prefectures('tokyo', 'eng')
        self.assertEqual(1, len(prefectures))
        self.assertEqual('tokyo to', prefectures[0].eng.lower())

    def test_cities(self):
        pref = self.postman.search_prefectures('東京', 'kanji')[0]
        cities = self.postman.cities(pref)
        self.assertEqual(62, len(cities))  # 07/19/2022
        self.assertEqual(pref, cities[0].prefecture)  # 07/19/2022

    def test_search_cities(self):
        tokyo = self.postman.search_prefectures('東京', 'kanji')[0]
        osaka = self.postman.search_prefectures('大阪', 'kanji')[0]
        cities = self.postman.search_cities('大阪市都島区')
        self.assertEqual(1, len(cities))
        self.assertEqual(osaka, cities[0].prefecture)

        cities = self.postman.search_cities('大阪市都島区', prefecture=tokyo)
        self.assertEqual(0, len(cities))

    def test_addresses(self):
        tokyo = self.postman.search_prefectures('東京', 'kanji')[0]
        cities = self.postman.search_cities('新宿', prefecture=tokyo)
        self.assertEqual(1, len(cities))
        city = cities[0]

        addresses = self.postman.addresses(city)
        self.assertEqual(696, len(addresses))  # 07/19/2022
        self.assertEqual(city, addresses[0].city)

    def test_search_addresses(self):
        tokyo = self.postman.search_prefectures('東京', 'kanji')[0]
        osaka = self.postman.search_prefectures('大阪', 'kanji')[0]
        cities = self.postman.search_cities('新宿', prefecture=tokyo)
        self.assertEqual(1, len(cities))
        city = cities[0]

        addresses = self.postman.search_addresses('歌舞伎町', city=city)
        self.assertEqual(1, len(addresses))
        address = addresses[0]
        self.assertEqual('歌舞伎町', address.kanji)
        self.assertEqual('新宿区', address.city.kanji)
        self.assertEqual('東京都', address.prefecture.kanji)
        self.assertEqual('東京都　新宿区　歌舞伎町', address.concat_kanji)
        self.assertEqual('トウキョウト　シンジュクク　カブキチョウ', address.concat_kana)
        self.assertEqual('Kabukicho, Shinjuku Ku, Tokyo To', address.concat_eng)

        self.assertRaises(ValueError, self.postman.search_addresses, '歌舞伎町', city=city, prefecture=osaka)
        addresses = self.postman.search_addresses('歌舞伎町', prefecture=osaka)
        self.assertEqual(0, len(addresses))


if __name__ == "__main__":
    unittest.main()
