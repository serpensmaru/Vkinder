
from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, DateTime, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from creation_db import create_database

# Авторизация в базе данных
password = input('Введите пароль пользователя postgres: ')
db_name = input('Введите название базы данных: ')

# Создание базы данных
Base = declarative_base()
create_database(password, db_name)

# Создание движка
engine = create_engine(f'postgresql+psycopg2://postgres:{password}@localhost:5432/{db_name}', echo=True)
engine.connect()

# Создание таблиц

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)


class Match(Base):
    __tablename__ = 'match'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    link = Column(String(100), nullable=False)
    photo = relationship("Photo")


user_match = Table('user_match', Base.metadata,
    Column('user_id', Integer(), ForeignKey("user.id")),
    Column('match_id', Integer(), ForeignKey("match.id"))
)


class Photo(Base):
    __tablename__ = 'photo'
    id = Column(Integer, primary_key=True)
    attachment = Column(String(100), nullable=False)
    match_id = Column(Integer, ForeignKey('match.id'))


Base.metadata.create_all(engine)


