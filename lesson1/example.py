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

cur.execute('INSERT INTO todos VALUES (3, False);')

cur.execute('INSERT INTO todos VALUES (%s, %s);', (1, True))

SQL = 'INSERT INTO todos VALUES (%(id)s, %(completed)s);'

data = {
    'id': 2,
    'completed': False}

cur.execute(SQL, data)

cur.execute('SELECT * FROM todos;')

result1 = cur.fetchmany(2)
print(f'result1: {result1}')

result2 = cur.fetchone()
print(f'result2: {result2}')

result3 = cur.fetchall()
print(f'result3: {result3}')

conn.commit()

cur.close()
conn.close()