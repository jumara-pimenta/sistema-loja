import psycopg2


def open_connection():
    try:
        connection = psycopg2.connect(
            host='localhost',
            database='postgres',
            port='5432',
            user='postgres',
            password='123456',
        )
        return connection
    except psycopg2.Error as e:
        print(f'Erro ao conectar no banco de dados: {e}')