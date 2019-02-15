from PyQt5.QtSql import QSqlQuery
import os
from datetime import date

import libro.queries as queries
import libro.config as config
from libro.utils.metadata import Metadata


class BookInfo:
    __slots__ = ['id', 'title', 'author', 'series', 'series_index', 'tags', 'type', 'lang', 'date_added', 'file']


def get_book_info(id):
    q = QSqlQuery(config.db)
    q.prepare(queries.SELECT_BOOK_INFO)
    q.bindValue(0, id)
    q.exec()
    if q.next():
        b = BookInfo()
        b.id = q.value(0)
        b.title = q.value(1)
        b.author = q.value(2)
        b.series = q.value(3)
        b.series_index = q.value(4)
        b.tags = q.value(5)
        b.lang = q.value(6)
        b.type = q.value(7)
        b.date_added = q.value(8)
        b.file = q.value(9)

        return b
    else:
        return None


def delete_book(id):
    q = QSqlQuery(config.db)
    q.prepare(queries.DELETE_BOOK)
    q.bindValue(0, id)
    q.exec()
    config.db.commit()


def add_book(file):
    file = os.path.normpath(file)
    try:
        meta = Metadata(file)
        meta.get_metadata(read_cover_image=False)
        cur_date = date.today().strftime('%d.%m.%Y')
        q = QSqlQuery(config.db)
        q.prepare(queries.INSERT_BOOK)
        q.bindValue(0, meta.title)
        q.bindValue(1, meta.author)
        q.bindValue(2, meta.tags)
        q.bindValue(3, meta.series)
        q.bindValue(4, meta.series_index)
        q.bindValue(5, meta.lang)
        q.bindValue(6, meta.type)
        q.bindValue(7, cur_date)
        q.bindValue(8, file)
        if not q.exec():
            print(q.lastError().text())
            config.db.rollback()
        else:
            config.db.commit()
    except Exception as e:
        print('{}: {}'.format(file, e))


def is_created():
    rows = -1
    q = QSqlQuery(config.db)
    q.exec(queries.CHECK_DB_CREATED)
    if q.next():
        rows = q.value(0)

    return rows == 1


def create():
    q = QSqlQuery(config.db)
    sql_lines = queries.CREATE_DB.split(';')
    for sql_line in sql_lines:
        if len(sql_line.strip()) > 0:
            if not q.exec(sql_line):
                print(q.lastError().text())

    if not q.exec(queries.TRIGGER_AI):
        print(q.lastError().text())
    if not q.exec(queries.TRIGGER_AD):
        print(q.lastError().text())
    if not q.exec(queries.TRIGGER_AU):
        print(q.lastError().text())
