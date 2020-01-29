# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from scrapy.utils.project import get_project_settings

from geekjob.models import (
    Vacancy,
    db_connect,
    create_table,
    check_existence_row_in_db,
    get_value_from_databse,
    update_values
)


class GeekjobPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        VacancyDB = Vacancy()
        VacancyDB.link = item['link']
        VacancyDB.title = item['title']
        VacancyDB.description = item['description']
        try:
            if check_existence_row_in_db(VacancyDB.link):
                columns_vacancy_db = [
                    i for i in dir(VacancyDB)
                    if not i.startswith('_') and i != 'metadata' and i != 'id' and i != 'created_at'\
                    and i != 'listing_id'
                ]
                if get_project_settings().get('UPDATE_VALUES_IN_DATABASE'):
                    for column in columns_vacancy_db:
                        if getattr(VacancyDB, column) != getattr(get_value_from_databse(VacancyDB.link), column):
                            print(
                                getattr(VacancyDB, column), '||||', getattr(get_value_from_databse(VacancyDB.link), column)
                            )
                            result = {
                                'link': VacancyDB.link,
                                'title': VacancyDB.title,
                                'description': VacancyDB.description
                            }
                            update_values(VacancyDB.link, result)
            else:
                session.add(VacancyDB)
                session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
