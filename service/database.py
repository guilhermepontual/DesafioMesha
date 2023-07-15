import psycopg2

database = 'railway'
user = 'postgres'
password = '0zf7kRbEdm4MouaovVXV'
host = 'containers-us-west-41.railway.app'
port = '6597'


conn = psycopg2.connect(
        dbname=database,
        user=user,
        password=password,
        host=host,
        port=port
)