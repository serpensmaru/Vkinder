from sqlalchemy import create_engine, Integer, Column, ForeignKey, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base_model = declarative_base()

# Таблицы
class User(Base_model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)


class Favour(Base_model):
    __tablename__ = 'favour'
    id = Column(Integer, primary_key=True)
    favour_id = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    favour = relationship('User')
    # user_id = Column(Integer)


class Swipe(Base_model):
    __tablename__ = 'swipe'
    id = Column(Integer, primary_key=True)
    swipe_id = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    swipe = relationship('User')
    # user_id = Column(Integer)


# Созадие движка
def engine_driv(user_db_name, password, db_name, log=True):
    engine = create_engine(f'postgresql+psycopg2://{user_db_name}:{password}@localhost:5432/{db_name}', echo=log)
    return engine


def sql_user_id(id_user, table_cl):
    """ Формрование sql запроса"""
    table = insert(table_cl).values(user_id=id_user)
    return table


def inserting(engine, sql):
    """ Отправка sql запроса"""
    with engine.connect() as conn:
        conn.execute(sql)


def bool_user_id(id_user, engine, table_cl):
    """ Проверяет наличие id в таблице"""
    ses = sessionmaker(bind=engine)
    session = ses()
    res = session.query(table_cl).filter_by(user_id=id_user).all() is not None
    return res


def bool_swipe_id(id_swipe, user_id, engine, table_cl):
    """ Проверяет наличие id в таблице"""
    ses = sessionmaker(bind=engine)
    session = ses()
    res = session.query(table_cl).filter_by(swipe_id=id_swipe, user_id=user_id).first() is not None
    return res


def if_not_add_user_id(id_user, engine, table_cl):
    """ Добавляет пользователя в БД, если его там нет"""
    if not (bool_user_id(id_user, engine, table_cl)):
        sql = sql_user_id(id_user, table_cl)
        inserting(engine, sql)
        return "User add database"


def add_swipe(id_user, id_swipe, engine):
    sql = insert(Swipe).values(user_id=id_user, swipe_id=id_swipe)
    inserting(engine, sql)


def add_favour(id_user, id_favour, engine):
    sql = insert(Favour).values(user_id=id_user, favour_id=id_favour)
    inserting(engine, sql)


def get_favour_id(engine, user_id):
    ses = sessionmaker(bind=engine)
    session = ses()
    q = session.query(Favour).filter(Favour.user_id == user_id)
    list_favout_id = [x.favour_id for x in q]
    return list_favout_id


def clear_sewipe(engine, id_user):
    ses = sessionmaker(bind=engine)
    session = ses()
    session.query(Swipe).filter(Swipe.user_id == id_user).delete()
    session.commit()


def del_favour(engine, id_user, id_favour):
    ses = sessionmaker(bind=engine)
    session = ses()
    session.query(Favour).filter(Favour.user_id == id_user, Favour.favour_id == id_favour).delete()
    session.commit()
