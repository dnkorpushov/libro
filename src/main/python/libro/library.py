from PyQt5.QtSql import QSqlQuery

import os

from datetime import date

import libro.queries as queries
import libro.config as config
from libro.utils.metadata import get_metadata, set_metadata


class BookRec:
    __slots__ = ['id', 'title', 'author', 'author_sort', 'series', 'series_index',
                 'tags', 'type', 'lang', 'translator', 'date_added',
                 'cover_image', 'file']


def get_book_info(id):
    q = QSqlQuery(config.db)
    q.prepare(queries.SELECT_BOOK_INFO)
    q.bindValue(0, id)
    q.exec_()
    if q.next():
        file = q.value(0)
        meta = get_metadata(file)
        meta.id = id
        return meta
    else:
        return None


def get_book_rec(id):
    q = QSqlQuery(config.db)
    q.prepare(queries.SELECT_BOOK_REC)
    q.bindValue(0, id)
    q.exec_()
    if q.next():
        b = BookRec()
        b.id = q.value(0)
        b.title = q.value(1)
        b.author = q.value(2)
        b.author_sort = q.value(3)
        b.series = q.value(4)
        b.tags = q.value(5)
        b.lang = q.value(6)
        b.translator = q.value(7)
        b.type = q.value(8)
        b.date_added = q.value(9)
        b.file = q.value(10)

        return b
    else:
        return BookRec()


def update_book_info(book_meta):
    set_metadata(book_meta)
    q = QSqlQuery(config.db)
    q.prepare(queries.UPDATE_BOOK)
    q.bindValue(0, book_meta.title)
    q.bindValue(1, book_meta.get_author_string(name_format='{#f {#m }}#l'))
    q.bindValue(2, book_meta.get_author_string(name_format='#l{ #f{ #m}}'))
    q.bindValue(3, book_meta.get_tag_string())
    q.bindValue(4, book_meta.series)
    q.bindValue(5, book_meta.series_index)
    q.bindValue(6, book_meta.lang)
    q.bindValue(7, book_meta.get_translator_string())
    q.bindValue(8, book_meta.book_format)
    q.bindValue(9, book_meta.id)
    if not q.exec_():
        print(q.lastError().text())
        config.db.rollback()
    else:
        config.db.commit()


def delete_book(id):
    q = QSqlQuery(config.db)
    q.prepare(queries.DELETE_BOOK)
    q.bindValue(0, id)
    if not q.exec_():
        print(q.lastError().text())
        config.db.rollback()
    else:
        config.db.commit()


def add_book(file):
    file = os.path.normpath(file)
    try:
        meta = get_metadata(file)
        cur_date = date.today().strftime('%d.%m.%Y')
        q = QSqlQuery(config.db)
        q.prepare(queries.INSERT_BOOK)
        q.bindValue(0, meta.title)
        q.bindValue(1, meta.get_author_string(name_format='{#f {#m }}#l'))
        q.bindValue(2, meta.get_author_string(name_format='#l{ #f{ #m}}'))
        q.bindValue(3, meta.get_tag_string())
        q.bindValue(4, meta.series)
        q.bindValue(5, meta.series_index)
        q.bindValue(6, meta.lang)
        q.bindValue(7, meta.get_translator_string())
        q.bindValue(8, meta.book_format)
        q.bindValue(9, cur_date)
        q.bindValue(10, file)
        if not q.exec_():
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
