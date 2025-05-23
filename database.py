import sqlite3

connection = sqlite3.connect('records.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY,
    date TEXT,
    path TEXT,
    method1 INTEGER,
    method2 INTEGER,
    method3 INTEGER
)
''')

connection.commit()

def add_record(date, path, counts):
    cursor.execute('INSERT INTO records (date, path, method1, method2, method3) VALUES (?, ?, ?, ?, ?)', 
                   (date, path, *counts)
    )
    connection.commit()

def get_all_records():
    cursor.execute('SELECT * FROM records')
    rows = cursor.fetchall() 
    return rows

def get_records_index(id_from, id_to):
    cursor.execute('SELECT * FROM records WHERE id >= ? and id <= ?', (id_from, id_to))
    rows = cursor.fetchall()   
    return rows