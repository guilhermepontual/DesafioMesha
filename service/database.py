import psycopg2

database = ''
user = ''
password = ''
host = ''
port = ''

conn = psycopg2.connect(
        dbname=database,
        user=user,
        password=password,
        host=host,
        port=port
)
