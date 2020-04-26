import psycopg2

conn = psycopg2.connect('dbname=todoapp_development user=darius')

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS todos;")

cur.execute("""
    CREATE TABLE todos (
        id serial PRIMARY KEY,
        description VARCHAR NOT NULL
    );
""")

cur.execute("""
    INSERT INTO todos
    VALUES (1, 'test entry');
""")


conn.commit()

cur.close()
conn.close()