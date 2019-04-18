import textwrap
from datetime import date, timedelta

from PyQt5.QtWidgets import QTableView, QAbstractItemView
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtSql import QSqlTableModel

import libro.config as config
import libro.library as library

_tr = QCoreApplication.translate


class BookTableView(QTableView):
    def __init__(self, parent=None):
        super(BookTableView, self).__init__(parent)

        font = self.font()
        fm = QFontMetrics(font)
        self.verticalHeader().setDefaultSectionSize(fm.height() + 8)

        self.setWordWrap(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setHighlightSections(False)

        self.setSortingEnabled(True)

    def init(self, db, columnsWidth):
        model = BookTableModel(db=db)
        model.setTable('v_book')
        model.setSort(1, Qt.AscendingOrder)
        self.horizontalHeader().setSortIndicator(1, Qt.AscendingOrder)
        model.select()
        model.setHeaderData(0, Qt.Horizontal, _tr('table', 'Id'))
        model.setHeaderData(1, Qt.Horizontal, _tr('table', 'Title'))
        model.setHeaderData(2, Qt.Horizontal, _tr('table', 'Author'))  # author column
        model.setHeaderData(3, Qt.Horizontal, _tr('table', 'Author'))  # author_sort column
        model.setHeaderData(4, Qt.Horizontal, _tr('table', 'Series'))
        model.setHeaderData(5, Qt.Horizontal, _tr('table', 'Tags'))
        model.setHeaderData(6, Qt.Horizontal, _tr('table', 'Lang'))
        model.setHeaderData(7, Qt.Horizontal, _tr('table', 'Translator'))
        model.setHeaderData(8, Qt.Horizontal, _tr('table', 'Type'))
        model.setHeaderData(9, Qt.Horizontal, _tr('table', 'Date added'))
        model.setHeaderData(10, Qt.Horizontal, _tr('table', 'File'))
        self.setModel(model)

        self.hideColumn(0)
        self.hideColumn(7)
        self.hideColumn(10)
        if not config.is_library_mode:
            self.hideColumn(9)
        if config.ui_display_sort_author:
            self.hideColumn(2)
        else:
            self.hideColumn(3)

        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().hide()
        for i in range(len(columnsWidth)):
            self.setColumnWidth(i, columnsWidth[i])

    def getBooksId(self):
        books_id = []
        for i in range(self.model().rowCount()):
            books_id.append(self.model().record(i).field('id').value())
        return books_id

    def getSelectedBooksId(self):
        books_id = []
        rows = self.selectionModel().selectedRows()
        for row in rows:
            books_id.append(self.model().record(row.row()).field('id').value())
        return books_id

    def updateSelectedRows(self):
        rows = self.selectionModel().selectedRows()
        for row in rows:
            self.updateRow(row.row())

    def updateRow(self, row):
        record = self.model().record(row)
        bookInfo = library.get_book_rec(record.field('id').value())
        record.setValue('title', bookInfo.title)
        record.setValue('author', bookInfo.author)
        record.setValue('author_sort', bookInfo.author_sort)
        record.setValue('series', bookInfo.series)
        record.setValue('tags', bookInfo.tags)
        record.setValue('lang', bookInfo.lang)
        record.setValue('translator', bookInfo.translator)
        record.setValue('type', bookInfo.type)
        record.setValue('date_added', bookInfo.date_added)
        record.setValue('file', bookInfo.file)
        self.model().setRecord(row, record)

    def search(self, searchCriteria, collection):
        filterStr = ''
        if len(searchCriteria) > 0:
            filterStr = 'id in (select rowid FROM book_idx WHERE book_idx MATCH "{}")'.format(searchCriteria)

        if collection is not None:
            if filterStr:
                if (collection.type != library.CollectionType.System and
                        collection.id != library.SystemCollectionId.AllBooks):
                    filterStr += ' AND '

            if collection.type == library.CollectionType.System:
                if collection.id == library.SystemCollectionId.AddedToday:
                    cur_date = date.today().strftime('%d.%m.%Y')
                    filterStr += 'date_added = "{}"'.format(cur_date)

                elif collection.id == library.SystemCollectionId.AddedLastWeek:
                    cur_date = date.today()
                    date_list = [(cur_date - timedelta(days=x)).strftime('%d.%m.%Y') for x in range(0, 7)]
                    list_str = ', '.join(map(lambda x: '\'' + x + '\'', date_list))
                    filterStr += 'date_added in ({})'.format(list_str)

            elif collection.type == library.CollectionType.Collection:
                filterStr += 'id in (select book_id from collection_book where collection_id = {})'.format(collection.id)

            elif collection.type == library.CollectionType.Smart:
                filterStr += 'id in (select rowid FROM book_idx WHERE book_idx MATCH "{}")'.format(collection.criteria)

        self.model().setFilter(filterStr)
        self.model().select()


class BookTableModel(QSqlTableModel):
    def __init__(self, parent=None, db=None):
        super(BookTableModel, self).__init__(parent=parent, db=db)
        self.setEditStrategy(QSqlTableModel.OnManualSubmit)

    def data(self, idx, role):
        if role == Qt.ToolTipRole:
            tooltipString = super(BookTableModel, self).data(idx, Qt.DisplayRole)
            return '\n'.join(textwrap.wrap(tooltipString, 70, break_long_words=False))
        else:
            return super(BookTableModel, self).data(idx, role)
