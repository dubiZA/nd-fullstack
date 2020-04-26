import psycopg2

conn = psycopg2.connect('dbname=todoapp_development user=darius')

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS todos;')

cur.execute('''
    CREATE TABLE todos (
        id INTEGER PRIMARY KEY,
        completed BOOLEAN NOT NULL DEFAULT False
    );
''')

cur.execute('INSERT INTO todos VALUES (%s, %s);', (1, True))

SQL = 'INSERT INTO todos VALUES (%(id)s, %(completed)s);'

data = {
    'id': 2,
    'completed': False}

cur.execute(SQL, data)

conn.commit()

cur.close()
conn.close()