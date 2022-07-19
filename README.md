Easy wrapper for the zip code data of Japan
-----------
Powered by [Yamato Nagata](https://twitter.com/514YJ)

# Installation
install with pip

```$ pip install jusho```

[GitHub](https://github.com/nagataaaas/Jusho)

# Example
Useful example [HERE](https://github.com/nagataaaas/Jusho/tree/main/example/example1)

![demo](https://github.com/nagataaaas/Jusho/blob/main/static/example1.gif?raw=true)

```python
from jusho import Jusho, Address, City, Prefecture

postman = Jusho()

print(postman.by_zip_code('160-0021'))  # '1600021', '〒1600021' and whatever is valid
# [Address(id=116156, city=City(id=1972, prefecture=Prefecture(id=36, kanji='東京都', kana='トウキョウト', eng='TOKYO T...

print(postman.prefectures)
# [Prefecture(id=0, kanji='北海道', kana='ホッカイドウ', eng='HOKKAIDO'), Prefecture(id=3, kanji='青森県', kana='アオモリケ...

osaka: Prefecture = postman.search_prefectures('大阪', 'kanji')[0]
print(postman.cities(osaka))
# [City(id=3613, prefecture=Prefecture(id=78, kanji='大阪府', kana='オオサカフ', eng='OSAKA FU'), kanji='大阪市都島区', ka...

shimamoto: City = postman.search_cities('三島郡島本町', prefecture=osaka)[0]
print(postman.addresses(shimamoto))
# [Address(id=264932, city=City(id=3799, prefecture=Prefecture(id=78, kanji='大阪府', kana='オオサカフ', eng='OSAKA FU'), kanji='三島郡島本町', kana='ミシマグンシマモトチョウ', eng='MISHIMA ...

aoba: Address = postman.search_addresses('青葉', city=shimamoto)[0]
# `postman.search_addresses('青葉', prefecture=osaka)`, `postman.search_addresses('青葉')` are also valid
# but the result is not the same.
print(aoba.hyphen_zip)
# 618-0015

"""
Address object has a lot of info
"""

admin_division_code: str = aoba.admin_division_code  # 27301

old_zip_code: str = aoba.old_zip_code  # 618

zip_code: str = aoba.zip_code  # 6180015

prefecture: Prefecture = aoba.prefecture  # Prefecture(id=78, kanji='大阪府', kana='オオサカフ', eng='OSAKA FU')

city: City = aoba.city  # City(id=3799, prefecture=Prefecture(id=78, kanji='大阪府', kana='オオサカフ', eng='OSAKA FU'), kanji='三島郡島本町', kana='ミシマグンシマモトチョウ', eng='MISHIMA GUN SHIMAMOTO CHO')

print('\n'.join((
    aoba.kanji,  # 青葉
    aoba.kana,  # アオバ
    aoba.eng,  # AOBA
    '--------',
    aoba.concat_kanji,  # 大阪府　三島郡島本町　青葉
    aoba.concat_kana,  # オオサカフ　ミシマグンシマモトチョウ　アオバ
    aoba.concat_eng,  # Aoba, Mishima Gun Shimamoto Cho, Osaka Fu
    '--------',
    aoba.city.kanji,  # 三島郡島本町
    aoba.city.kana,  # ミシマグンシマモトチョウ
    aoba.city.eng,  # MISHIMA GUN SHIMAMOTO CHO
    '--------',
    aoba.city.concat_kanji,  # 大阪府　三島郡島本町
    aoba.city.concat_kana,  # オオサカフ　ミシマグンシマモトチョウ
    aoba.city.concat_eng,  # Mishima Gun Shimamoto Cho, Osaka Fu
    '--------',
    aoba.prefecture.kanji,  # 大阪府
    aoba.prefecture.kana,  # オオサカフ
    aoba.prefecture.eng,  # OSAKA FU
)))

```

# TroubleShooting

## No database file found!
Database file is already included in the package.\
But in case `Jusho` can't find the database file, you can download it with `Jusho.create_database(path: str)`.

And then specify the path to the database file like `Jusho(database_path='/path/to/database.db')`.

```python

# data
data is from Japan Post
- https://www.post.japanpost.jp/zipcode/dl/kogaki/zip/ken_all.zip
- https://www.post.japanpost.jp/zipcode/dl/roman/ken_all_rome.zip