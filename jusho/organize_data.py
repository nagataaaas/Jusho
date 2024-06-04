import os
import shutil
import sqlite3
import tempfile
import urllib.request
from collections import defaultdict
from dataclasses import replace
from logging import getLogger, basicConfig
from typing import Tuple, Iterator, Dict, List

import jusho.gateway as gateway
from .models import Address, Prefecture, City, TABLE_COUNT

ken_all_url = 'https://www.post.japanpost.jp/zipcode/dl/kogaki/zip/ken_all.zip'
ken_all_rome_url = 'https://www.post.japanpost.jp/zipcode/dl/roman/KEN_ALL_ROME.zip'

basicConfig(level='INFO')
logger = getLogger(__name__)


def tqdm(iterable: Iterator) -> Tuple[int, str]:
    values = list(iterable)
    length = len(values)
    for i, v in enumerate(values):
        yield i, v
        percent = i / length * 100
        if i % int(length / 100) == 0:
            print('\r{}% | {}/{}'.format(int(percent), i + 1, length), end='')
    print('\r100% | {}/{}'.format(length, length))


def han_to_zen(text: str) -> str:
    zenkaku = {i: v for i, v in enumerate('、。「」　－０１２３４５６７８９'
                                          'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン'
                                          'ッァィゥェォャュョ'
                                          'ガギグゲゴザジズゼゾダヂヅデドバビブベボヴ'
                                          'パピプペポ（）ーａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ／＜＞・．')}

    hankaku = ('､｡｢｣ -0123456789'
               'ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜｦﾝ'
               'ｯｧｨｩｪｫｬｭｮ'
               'ｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾊﾋﾌﾍﾎｳ'
               'ﾊﾋﾌﾍﾎ()ｰabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/<>･.')
    dakuten, handakuten = 'ﾞﾟ'
    result = []
    i = 0
    max_index = len(text) - 1
    while i < len(text):
        c = text[i]
        index = hankaku.find(c)
        if index == -1:
            result.append(c)
            i += 1
        elif index == 18:
            if i != max_index and text[i + 1] == dakuten:
                result.append('ヴ')
                i += 2
            else:
                result.append('ウ')
                i += 1
        elif 21 <= index <= 35:  # ｶ-ｺ, ｻ-ｿ, ﾀ-ﾄ
            if i != max_index and text[i + 1] == dakuten:
                result.append(zenkaku[index + 50])
                i += 2
            else:
                result.append(zenkaku[index])
                i += 1
        elif 41 <= index <= 45:  # ﾊ-ﾎ
            if i != max_index and text[i + 1] == dakuten:
                result.append(zenkaku[index + 45])
                i += 2
            elif i != max_index and text[i + 1] == handakuten:
                result.append(zenkaku[index + 51])
                i += 2
            else:
                result.append(zenkaku[index])
                i += 1
        else:
            result.append(zenkaku[index])
            i += 1
    return ''.join(result)


def insert_data(database_path: str, ken_all_path: str, ken_all_rome_path: str):
    prefectures: Dict[str, Prefecture] = {}
    cities: Dict[str, City] = {}
    addr: Dict[str, Dict[str, List[Address]]] = defaultdict(lambda: defaultdict(list))

    with open(ken_all_path, 'r', encoding='shift-jis') as f:
        logger.info('parse ken_all.csv')
        for i, line in tqdm(f.read().splitlines()):
            (admin_division_code, old_zip_code, zip_code,
             prefecture_kana, city_kana, kana,
             prefecture_kanji, city_kanji, kanji,
             multiple_zip_code, multiple_address,
             has_chome, multiple_town_area, *_) = map(lambda x: x.strip('"'), line.split(','))

            old_zip_code = old_zip_code.strip()
            prefecture_kana = han_to_zen(prefecture_kana)
            city_kana = han_to_zen(city_kana)
            kana = han_to_zen(kana)

            if prefecture_kanji not in prefectures:
                prefectures[prefecture_kanji] = Prefecture(len(prefectures) * TABLE_COUNT, prefecture_kanji,
                                                           prefecture_kana, '')
            city_key = (prefecture_kanji + city_kanji).replace('　', '').replace('\u3000', '')
            if city_key not in cities:
                cities[city_key] = City(len(cities) * TABLE_COUNT + 1, prefectures[prefecture_kanji], city_kanji,
                                        city_kana, '')

            address = Address(
                id=i * TABLE_COUNT + 2,
                city=cities[city_key],
                admin_division_code=admin_division_code,
                old_zip_code=old_zip_code,
                zip_code=zip_code,
                kanji=kanji,
                kana=kana,
                eng='',
                multiple_zip_code=multiple_zip_code,
                multiple_address=multiple_address,
                has_chome=has_chome,
                multiple_town_area=multiple_town_area
            )
            key = (address.concat_kanji.replace('　', '').replace('\u3000', ''))
            addr[address.prefecture.kanji][key].append(address)

    with open(ken_all_rome_path, 'r', encoding='shift-jis') as f:
        logger.info('parse ken_all_rome.csv')
        for _, line in tqdm(f.read().splitlines()):
            zipcode, prefecture_kanji, city_kanji, kanji, pref_eng, city_eng, town_eng = map(lambda x: x.strip('"'),
                                                                                             line.split(','))

            if prefecture_kanji in prefectures and not prefectures[prefecture_kanji].eng:
                prefectures[prefecture_kanji] = replace(prefectures[prefecture_kanji], eng=pref_eng)

            city_key = (prefecture_kanji + city_kanji).replace('　', '').replace('\u3000', '')
            if city_key in cities and not cities[city_key].eng:
                cities[city_key] = replace(cities[city_key], eng=city_eng)

            key = f'{prefecture_kanji}{city_kanji}{kanji}'.replace('　', '').replace('\u3000', '')
            if key in addr[prefecture_kanji]:
                ads = addr[prefecture_kanji][key]
            else:
                for k, v in addr[prefecture_kanji].items():
                    if k.startswith(key):
                        ads = v
                        break
                    if any(ad.zip_code == zipcode for ad in v):
                        ads = v
                        break
                else:
                    continue
            for i, ad in enumerate(ads):
                if not ad.eng:
                    ads[i] = replace(ad, eng=town_eng)

    if os.path.exists(database_path):
        os.remove(database_path)
    conn = sqlite3.connect(database_path)

    c = conn.cursor()
    c.executescript(gateway.insert.CREATE_TABLES)

    conn.commit()
    for pref in prefectures.values():
        gateway.insert.insert_prefecture(c, pref)
    for city in cities.values():
        gateway.insert.insert_city(c, city)
    for pref in addr.values():
        for ads in pref.values():
            for ad in ads:
                gateway.insert.insert_address(c, ad)

    conn.commit()
    conn.close()


def download_csv(output_dir):
    with tempfile.TemporaryDirectory() as tmp_dir:
        urllib.request.urlretrieve(ken_all_url, os.path.join(tmp_dir, 'ken_all.zip'))
        urllib.request.urlretrieve(ken_all_rome_url, os.path.join(tmp_dir, 'ken_all_rome.zip'))
        shutil.unpack_archive(os.path.join(tmp_dir, 'ken_all.zip'), output_dir)
        shutil.unpack_archive(os.path.join(tmp_dir, 'ken_all_rome.zip'), output_dir)


def create_database(database_path: str):
    if os.path.exists(database_path):
        os.remove(database_path)
    with tempfile.TemporaryDirectory() as tmp_dir:
        download_csv(tmp_dir)
        insert_data(database_path, os.path.join(tmp_dir, 'ken_all.csv'), os.path.join(tmp_dir, 'ken_all_rome.csv'))
