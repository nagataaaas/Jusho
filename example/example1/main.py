import responder
from jusho import Jusho

api = responder.API()
postman = Jusho()

katakana_chart = "ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶヽヾ"
hiragana_chart = "ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんゔゕゖゝゞ"
hir2kat = str.maketrans(hiragana_chart, katakana_chart)
kat2hir = str.maketrans(katakana_chart, hiragana_chart)


@api.route('/')
def index(req, resp):
    resp.html = api.template('index.html')


@api.route('/api/pref')
async def pref(req, resp):
    user_input = (await req.media(format='json'))['pref']
    user_input = user_input.translate(hir2kat).upper()
    prefs = set()
    for type_ in ['kanji', 'kana', 'eng']:
        data = postman.search_prefectures(user_input, type_)
        if data:
            prefs.update(data)
    resp.media = {'similar': [{'name': p.kanji, 'id': p.id} for p in prefs]}


@api.route('/api/city')
async def pref(req, resp):
    data = await req.media(format='json')
    pref_id, user_city = data['pref'], data['city']
    pref = postman.prefecture_by_id(int(pref_id))
    user_city = user_city.translate(hir2kat).upper()
    cities = set()
    for type_ in ['kanji', 'kana', 'eng']:
        data = postman.search_cities(user_city, pref, type_)
        if data:
            cities.update(data)
    resp.media = {'similar': [{'name': c.kanji, 'id': c.id} for c in cities]}


@api.route('/api/town')
async def pref(req, resp):
    data = await req.media(format='json')
    city_id, user_town = data['city'], data['town']
    city = postman.city_by_id(int(city_id))
    user_town = user_town.translate(hir2kat).upper()

    towns = set()
    for type_ in ['kanji', 'kana', 'eng']:
        data = postman.search_addresses(user_town, city=city, type_=type_)
        if data:
            towns.update(data)
    resp.media = {'similar': [{'name': t.kanji, 'id': t.id} for t in towns]}


@api.route('/api/zip')
async def pref(req, resp):
    data = await req.media(format='json')
    town_id = data['town']
    town = postman.address_by_id(int(town_id))
    resp.media = {'zip': town.hyphen_zip}


if __name__ == '__main__':
    api.run()
