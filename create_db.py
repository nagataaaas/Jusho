import sqlite3
conn = sqlite3.connect('jusho/address.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE address
             (admin_division_code text, old_postal_code text, postal_code text,
              prefecture_kana text, city_kana text, town_area_kana text, 
              prefecture_kanji text, city_kanji text, town_area_kanji text, 
              prefecture_eng text, city_eng text, town_area_eng text,
              multiple_postal_code integer, multiple_address integer, 
              has_chome integer, multiple_town_area integer)''')

c.execute("create index postal_code_index on address(postal_code)")
c.execute("create index prefecture_kana_index on address(prefecture_kana)")
c.execute("create index city_kana_index on address(city_kana)")
c.execute("create index town_area_kana_sindex on address(town_area_kana)")
c.execute("create index prefecture_kanji_index on address(prefecture_kanji)")
c.execute("create index city_kanji_index on address(city_kanji)")
c.execute("create index town_area_kanji_index on address(town_area_kanji)")
c.execute("create index prefecture_eng_index on address(prefecture_eng)")
c.execute("create index city_eng_index on address(city_eng)")
c.execute("create index town_area_eng_index on address(town_area_eng)")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()