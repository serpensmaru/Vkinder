import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_database(db_name):
    # Устанавливаем соединение с postgres
    connection = psycopg2.connect(user='postgres', password="123456")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # Создаем курсор для выполнения операций с базой данных
    cursor = connection.cursor()
    sql_create_database = cursor.execute(f'create database {db_name}')
    # Создаем базу данных

    # Закрываем соединение
    cursor.close()
    connection.close()
    return db_name
