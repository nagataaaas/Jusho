import responder
from jusho import Jusho

api = responder.API()
postman = Jusho()

katakana_chart = "ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶヽヾ"
hiragana_chart = "ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんゔゕゖゝゞ"
hir2kat = str.maketrans(hiragana_chart, katakana_chart)
kat2hir = str.maketrans(katakana_chart, hiragana_chart)


@api.route('/api/postal')
async def pref(req, resp):
    data = await req.media(format='json')
    user_pref, user_city, user_town = data['pref'], data['city'], data['town']
    resp.media = {'postal': postman.address_from_town(user_pref, user_city, user_town, 'kanji').hyphen_postal}

@api.route('/api/pref')
async def pref(req, resp):
    user_input = (await req.media(format='json'))['pref']
    user_input = user_input.translate(hir2kat).upper()
    similar = []
    for pref in postman.prefectures:
        for val in pref:
            if val.startswith(user_input):
                similar.append([pref[1], pref[1]])
                break
    resp.media = {'similar': similar}

@api.route('/api/city')
async def pref(req, resp):
    data = await req.media(format='json')
    user_pref, user_city = data['pref'], data['city']
    user_pref = user_pref.translate(hir2kat).upper()
    user_city = user_city.translate(hir2kat).upper()
    similar = []
    for city in postman.cities_from_prefecture(user_pref, 'kanji'):
        for val in city:
            if val.startswith(user_city):
                similar.append([city[1], city[1]])
                break
    resp.media = {'similar': similar}

@api.route('/api/town')
async def pref(req, resp):
    data = await req.media(format='json')
    user_pref, user_city, user_town = data['pref'], data['city'], data['town']
    user_pref = user_pref.translate(hir2kat).upper()
    user_city = user_city.translate(hir2kat).upper()
    user_town = user_town.translate(hir2kat).upper()
    similar = []
    for town in postman.towns_from_city(user_pref, user_city, 'kanji'):
        for val in (town.town_area_eng, town.town_area_kanji, town.town_area_kana):
            if val.startswith(user_town):
                similar.append([town.town_area_kanji, town.town_area_kanji])
                break
    resp.media = {'similar': similar}


@api.route('/')
def index(req, resp):
    resp.html = api.template('index.html')


if __name__ == '__main__':
    api.run()
