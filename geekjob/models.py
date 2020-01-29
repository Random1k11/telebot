# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker
from scrapy.utils.project import get_project_settings
import datetime


Base = declarative_base()


def db_connect():
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


engine = db_connect()
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()


class Vacancy(Base):

    __tablename__ = 'vacancy'

    id = Column(Integer, primary_key=True)
    link = Column(String(2048))
    title = Column(String(500))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<Title: {}, URL: {}>'.format(self.title, self.URL)


def check_existence_row_in_db(link):
    return session.query(Vacancy).filter(Vacancy.link == link).first()


def get_value_from_databse(link):
    return session.query(Vacancy).filter(Vacancy.link == link).first()


def update_values(link, result):
    session.query(Vacancy).filter(Vacancy.link == link).update(
        dict(
            link=result['link'],
            title=result['title'],
            description=result['description'],
            created_at=datetime.datetime.now()
        )
    )
    session.commit()
