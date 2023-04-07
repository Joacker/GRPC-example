from psycopg2 import connect

def get_db():
    conn = connect(
        dbname="proyecto",
        user="postgres",
        password="postgres",
        host="postgres",
        port = 5432
    )
    return conn