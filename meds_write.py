from bs4 import BeautifulSoup #pip install beautifulsoup4
import requests
import sqlite3

db_file = 'database.db'
schema_file = 'schema.sql'

with open(schema_file, 'r') as rf:
    schema = rf.read()

url = "https://www.formulary.health.gov.on.ca/formulary/results.xhtml?q=keflex&type=2"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

medications = doc.find_all(["tr"], class_="ui-widget-content")
# 0: DIN, 1: Generic, 2: Brand, 3: MFR, 4: price, 5: MOH_coverage, 6: interch, 7: LU, 8: tx notes

meds_data = {'din':[], 'generic':[], 'brand':[], 'price':[], 'moh':[], 'lu':[]} 

for med in medications:
    meds_data['din'].append(med.contents[0].find(['a']).string)
    meds_data['generic'].append(med.contents[1].string)
    meds_data['brand'].append(med.contents[2].string)
    meds_data['price'].append(med.contents[4].string)
    meds_data['moh'].append(med.contents[5].string)
    meds_data['lu'].append(med.contents[7].string)

with sqlite3.connect(db_file) as conn:
    conn.executescript(schema)
    for i in range(len(meds_data['din'])):
        conn.execute("INSERT INTO meds (din, generic, brand, price, moh, lu) VALUES (?, ?, ?, ?, ?, ?)", 
                        (meds_data['din'][i], 
                            meds_data['generic'][i],
                            meds_data['brand'][i], 
                            meds_data['price'][i],
                            meds_data['moh'][i],
                            meds_data['lu'][i]))
