# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from scrapy.utils.project import get_project_settings
import sys
import os


Base = declarative_base()


def db_connect():
    return create_engine('sqlite:////home/dima/Desktop/geekjob/geekjob/geekjob.db')


engine = db_connect()
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()


result = engine.execute('SELECT * FROM "VACANCY"')
for r in result:
   print(r)