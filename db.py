from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Boolean, PickleType
from loguru import logger


class DB:
    @logger.catch
    def __init__(self, DATABASE_FILE):
        self.engine = create_engine(f"sqlite:////home/igor/PycharmProjects/4semProject/debugger/{DATABASE_FILE}")
        Session = sessionmaker(bind=self.engine)
        self.Base = declarative_base()
        self.s = Session()
        logger.success(f"База данных активирована по адресу: {DATABASE_FILE}")

    @logger.catch
    def setup(self):
        self.Base.metadata.create_all(self.engine)
        logger.success("Таблица БД создана")

    @logger.catch
    def merge(self, data):
        self.s.merge(data)
        logger.info(f"В соединение был добавлен объект таблицы {data.__class__.__tablename__}, "
                    f"id={data.id if data.id else data}")

    @logger.catch
    def commit(self):
        self.s.commit()
        logger.info("Произошёл коммит в БД")


db = DB("db.db")


class Users(db.Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    answers = Column(PickleType)
    is_admin = Column(Boolean, default=False)


class Manage(db.Base):
    __tablename__ = "manage"
    id = Column(Integer, primary_key=True, default=1)
    short_name = Column(String)
    questions = Column(PickleType)

db.setup()