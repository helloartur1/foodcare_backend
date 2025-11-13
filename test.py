import psycopg2

dsn = "host=localhost dbname=postgres user=postgres password=12345 port=5433"

try:
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    cur.execute("SELECT version();")
    print(cur.fetchone())
    conn.close()
except Exception as e:
    print("Ошибка подключения:", repr(e))
