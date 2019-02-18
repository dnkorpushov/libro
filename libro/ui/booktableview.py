import textwrap

from PyQt5.QtWidgets import QTableView, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtSql import QSqlTableModel

import libro.config as config


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
        self.setAlternatingRowColors(False)
        self.horizontalHeader().setHighlightSections(False)

        self.setSortingEnabled(True)

    def init(self, db, columnsWidth):
        model = BookTableModel(db=db)
        model.setTable('v_book')
        model.setSort(1, Qt.AscendingOrder)
        self.horizontalHeader().setSortIndicator(1, Qt.AscendingOrder)
        model.select()
        model.setHeaderData(0, Qt.Horizontal, 'Id')
        model.setHeaderData(1, Qt.Horizontal, 'Title')
        model.setHeaderData(2, Qt.Horizontal, 'Author')
        model.setHeaderData(3, Qt.Horizontal, 'Series')
        model.setHeaderData(4, Qt.Horizontal, 'Tags')
        model.setHeaderData(5, Qt.Horizontal, 'Lang')
        model.setHeaderData(6, Qt.Horizontal, 'Type')
        model.setHeaderData(7, Qt.Horizontal, 'Date added')
        model.setHeaderData(8, Qt.Horizontal, 'File')
        self.setModel(model)

        self.hideColumn(0)
        self.hideColumn(8)
        if not config.library_mode:
            self.hideColumn(7)

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

    def search(self, searchCriteria):
        if len(searchCriteria) > 0:
            filterStr = 'id in (select rowid FROM book_idx WHERE book_idx MATCH "{}")'.format(searchCriteria)
            self.model().setFilter(filterStr)
        else:
            self.model().setFilter('')
        self.model().select()


class BookTableModel(QSqlTableModel):
    def __init__(self, parent=None, db=None):
        super(BookTableModel, self).__init__(parent=parent, db=db)

    def data(self, idx, role):
        if role == Qt.ToolTipRole:
            tooltipString = super(BookTableModel, self).data(idx, Qt.DisplayRole)
            return '\n'.join(textwrap.wrap(tooltipString, 70, break_long_words=False))
        else:
            return super(BookTableModel, self).data(idx, role)
