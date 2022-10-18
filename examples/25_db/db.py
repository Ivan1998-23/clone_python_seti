import sqlite3
from pprint import pprint

connection = sqlite3.connect('new_db.db')
cursor = connection.cursor()
cursor.execute('select * from switch')
while True:
    three_rows = cursor.fetchmany(3)
    if three_rows:
        pprint(three_rows)
    else:
        break
