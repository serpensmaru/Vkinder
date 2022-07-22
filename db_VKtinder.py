from sqlalchemy import create_engine, MetaData, Table, Integer, Column, ForeignKey, insert, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, session, Session
import psycopg2
from module.PostgressVK import engine_driv, Base_model, Favour, Swipe, inserting, sql_user_id
# Авторизация в базе данных
password = "123456"
db_name = "vkinder"
user_db_name = "postgres"

# Создание базы данных
engine = engine_driv(user_db_name, password, db_name, log=False)
Base_model.metadata.create_all(engine)  #  Создание таблиц, если их нет

Session = sessionmaker(bind=engine)
session = Session()
# res = session.query(Favour).filter_by(user_id=id).first() is not None

# q = session.query(Favour).filter_by(user_id = 1111).first()
q = session.query(Favour).filter(Favour.user_id==173442120)
print(q)
for c in q:
    print(c.favour_id)

