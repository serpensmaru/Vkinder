from sqlalchemy import create_engine, MetaData, Table, Integer, Column, ForeignKey, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, session, Session
import psycopg2
from module.PostgressVK import engine_driv, Base_model, User, Favour, Swipe, insert_user_id, inserting, sql_user_id
# Авторизация в базе данных
password = "123456"
db_name = "vkinder"
user_db_name = "postgres"

# Создание базы данных
engine = engine_driv(user_db_name, password, db_name, log=False)
Base_model.metadata.create_all(engine)  #  Создание таблиц, если их нет


