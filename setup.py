"""
Easy wrapper for the postal code data of Japan
-----------
Powered by [Yamato Nagata](https://twitter.com/514YJ)

[GitHub](https://github.com/nagataaaas/Jusho)

Useful example [HERE](https://github.com/nagataaaas/Jusho/example/example1)

Using sqlite3 for the whole data. Runs really fast and uses less memory.

```python
from jusho import Jusho

postman = Jusho()

print(postman.from_postal_code('160-0021')) # '1600021', '〒1600021' and whatever is valid
  # 〒160-0021, 東京都 新宿区 歌舞伎町(TOKYO TO SHINJUKU KU KABUKICHO)

print(postman.prefectures)
  # [('アイチケン', '愛知県', 'AICHI KEN'), ('アオモリケン', '青森県', 'AOMORI KEN'), ('アキタケン', '秋田県', 'AKITA KEN'), ('イシカワケン', '石川県', 'ISHIKAWA KEN'), ('イバラキケン', '茨城県'...

print(postman.cities_from_prefecture('大阪府', type='kanji'))
  # [('ミシマグンシマモトチョウ', '三島郡島本町', 'MISHIMA GUN SHIMAMOTO CHO'), ('オオサカシミヤコジマク', '大阪市都島区', 'OSAKA SHI MIYAKOJIMA KU'), ('オオサカシフクシマク', '大阪市福島区', 'OSAK...

print(postman.towns_from_city('大阪府', '三島郡島本町', 'kanji'))
  # [<Address: 〒618-0000, 大阪府 三島郡島本町 以下に掲載がない場合(OSAKA FU MISHIMA GUN SHIMAMOTO CHO IKANIKEISAIGANAIBAAI)>, <Address: 〒618-0015, 大阪府 三島郡島本町 青葉(OSAKA FU MISHIMA GUN SHIMAMOTO CHO AOBA)>, <Address: 〒618-0013, 大阪府 三島郡島本町 江川(OSAK...

aoba = postman.address_from_town('大阪府', '三島郡島本町', '青葉', 'kanji')
print(aoba.hyphen_postal)
  # 618-0015

\"""
Address object has a lot of info
\"""

aoba.admin_division_code: str
  # 全国地方公共団体コード(Administrative divisions Code)
aoba.old_postal_code: str
  # the old postal code
aoba.postal_code: str
  # the postal code
aoba.prefecture_kana(_kanji, _eng): str
  # prefecture name in hiragana, kanji, and English
aoba.city_kana(_kanji, _eng): str
  # city name in hiragana, kanji, and English
aoba.town_area_kana(_kanji, _eng): str
  # town area name in hiragana, kanji, and English
aoba.multiple_postal_code: bool
  # whether the area has alter postal codes
aoba.multiple_address: bool
  # whether the postal code includes multiple `Banchi`
aoba.has_chome: bool
  # whether the area has `Chome` which means subdivided areas
aoba.multiple_town_area: bool
  # whether the postal code includes multiple areas

```
"""

from setuptools import setup
from os import path

about = {}
with open("jusho/__about__.py") as f:
    exec(f.read(), about)

here = path.abspath(path.dirname(__file__))

setup(name=about["__title__"],
      version=about["__version__"],
      url=about["__url__"],
      license=about["__license__"],
      author=about["__author__"],
      author_email=about["__author_email__"],
      description=about["__description__"],
      long_description=__doc__,
      long_description_content_type="text/markdown",
      packages=["jusho"],
      zip_safe=False,
      platforms="any",
      data_files=[
          ('data', ['jusho/data/address.db']),
      ],
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Other Environment",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules"
      ])
