# py file for testing, example keflex

import sqlite3

db_file = 'database.db'

with sqlite3.connect(db_file) as conn:
    c = conn.cursor()
    c.execute("SELECT * FROM meds")
    meds = c.fetchall()
    # 0: DIN, 1: Generic, 2: Brand, 3: price, 4: MOH_coverage, 5: LU

query = 'keflex'
query.lower()
results = {'din':[], 'generic':[], 'brand':[], 'price':[], 'moh':[], 'lu':[]} 

for med in meds:
    if query in (med[1] + med[2]).lower():
        if med[4].replace(".","").isnumeric() and med[5].replace(".","").isnumeric():
            price = float(med[4]) - float(med[5])
        else:
            price = 'not available'
        results['din'].append(med[0])
        results['generic'].append(med[1])
        results['brand'].append(med[2])
        results['price'].append(price)
        results['lu'].append(med[5])

print(results)
        
