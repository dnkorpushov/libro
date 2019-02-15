from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt


class BookTreeWidget(QTreeWidget):
    def __init__(self, parent):
        super(BookTreeWidget, self).__init__(parent)
        self.setRootIsDecorated(False)

        self.setSortingEnabled(True)
        self.sortByColumn(0, Qt.AscendingOrder)

    def setHeaders(self):
        self.headerItem().setText(0, 'Title')
        self.headerItem().setText(1, 'Author')
        self.headerItem().setText(2, 'Series')
        self.headerItem().setText(3, 'Tags')
        self.headerItem().setText(4, 'Lang')
        self.headerItem().setText(5, 'Type')
        self.headerItem().setText(6, 'Date added')
        self.headerItem().setText(7, 'File')

    def addBookItem(self, bookInfo):
        item = QTreeWidgetItem()
        item.setText(0, bookInfo.title)
        item.setText(1, bookInfo.author)
        if bookInfo.series:
            if bookInfo.series_index:
                series = '{} ({})'.format(bookInfo.series, bookInfo.series_index)
            else:
                series = bookInfo.series
            item.setText(2, series)
        item.setText(3, bookInfo.tags)
        item.setText(4, bookInfo.lang)
        item.setText(5, bookInfo.type)
        item.setText(6, bookInfo.date_added)
        item.setText(7, bookInfo.file)

        self.addTopLevelItem(item)
