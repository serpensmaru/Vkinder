from sqlalchemy import create_engine, MetaData, Table, Integer, Column, ForeignKey, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
import psycopg2

Base_model = declarative_base()
# Таблицы
# class User(Base_model):
#     __tablename__ = 'user'
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer)
#     swipe = relationship('Swipe')
#     favour = relationship('Favour')

class Favour(Base_model):
    __tablename__ = 'favour'
    id = Column(Integer, primary_key=True)
    favour_id = Column(Integer)
    # user_id = Column(Integer, ForeignKey('user.user_id'))
    user_id = Column(Integer)

class Swipe(Base_model):
    __tablename__ = 'swipe'
    id = Column(Integer, primary_key=True)
    swipe_id = Column(Integer)
    # user_id = Column(Integer, ForeignKey('user.user_id'))
    user_id = Column(Integer)

# Созадие движка
def engine_driv(user_db_name, password, db_name, log = True):
    engine = create_engine(f'postgresql+psycopg2://{user_db_name}:{password}@localhost:5432/{db_name}', echo=log)
    return engine

def insert_user_id(engine, x, y):
    """ Отправка sql запроса в 3 таблицы"""
    with engine.connect() as conn:
        conn.execute(x)
        conn.execute(y)

def sql_user_id(id, F=Favour, S=Swipe):
    """ Формрование sql запросы в три таблицы"""
    favour = insert(F).values(user_id=id)
    swipe = insert(S).values(user_id=id)
    return favour, swipe

def inserting(engine, sql):
    """ Отправка sql запроса"""
    with engine.connect() as conn:
        x = conn.execute(sql)

def bool_user_id(id, engine):
    """ Проверяет наличие id в таблице User"""
    Session = sessionmaker(bind=engine)
    session = Session()
    res = session.query(Favour).filter_by(user_id=id).first() is not None
    return res

def if_not_add_user_id(id_user, engine):
    """ Добавляет пользователя в БД, если его там нет"""
    if not (bool_user_id(id_user, engine)):
        x, y = sql_user_id(id_user)
        insert_user_id(engine, x, y)
        return "User add database"
