from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QStyledItemDelegate
from PyQt5.QtGui import QFontMetrics, QIcon
from PyQt5.QtCore import QSize, Qt

from libro.library import CollectionType, SystemCollectionId


class NavListWidget(QListWidget):
    def __init__(self, parent=None):
        super(NavListWidget, self).__init__(parent)
        self.setItemDelegate(CustomItemDelegate(self))
        self.setIconSize(QSize(16, 16))

    def addHeaderItem(self, text):
        item = QListWidgetItem(text)
        item.setData(Qt.UserRole, (CustomItemDelegate.HeaderItem, None))
        font = self.font()
        fm = QFontMetrics(font)
        item.setSizeHint(QSize(0, fm.height() + 16))
        item.setFont(font)
        super(NavListWidget, self).addItem(item)

    def updateItem(self, collection):
        for i in range(0, self.count()):
            item = self.item(i)
            (item_type, cur_collection) = item.data(Qt.UserRole)
            if item_type == CustomItemDelegate.Item and collection.id == cur_collection.id:
                item.setData(Qt.UserRole, (item_type, collection))
                item.setText(collection.name)
                break

    def removeItem(self, collection):
        for i in range(0, self.count()):
            item = self.item(i)
            (item_type, cur_collection) = item.data(Qt.UserRole)
            if item_type == CustomItemDelegate.Item and collection.id == cur_collection.id:
                self.takeItem(i)
                break

    def addItem(self, collection):
        item = QListWidgetItem(collection.name)
        item.setData(Qt.UserRole, (CustomItemDelegate.Item, collection))
        icon = None

        if collection.type == CollectionType.System:
            if collection.id == SystemCollectionId.AllBooks:
                icon = ':/nav/nav-all-books.png'
            elif collection.id == SystemCollectionId.AddedToday:
                icon = ':/nav/nav-added-today.png'
            elif collection.id == SystemCollectionId.AddedLastWeek:
                icon = ':/nav/nav-added-week.png'
        elif collection.type == CollectionType.Collection:
            icon = ':/nav/nav-collection.png'
        elif collection.type == CollectionType.Smart:
            icon = ':/nav/nav-smart-collection.png'

        font = self.font()
        fm = QFontMetrics(font)
        item.setSizeHint(QSize(0, fm.height() + 8))
        item.setIcon(QIcon(icon))
        super(NavListWidget, self).addItem(item)

    def getCollection(self, row):
        item = self.item(row)
        collection = item.data(Qt.UserRole)[1]
        return collection


class CustomItemDelegate(QStyledItemDelegate):
    HeaderItem = 0
    Item = 1

    def paint(self, painter, option, index):
        userData = index.data(Qt.UserRole)
        if userData[0] == self.HeaderItem:
            text = index.data(Qt.DisplayRole)
            font = index.data(Qt.FontRole)
            font.setBold(True)
            painter.setFont(font)
            rect = option.rect
            rect.adjust(3, 0, 0, 0)

            painter.drawText(rect, Qt.AlignLeft | Qt.AlignVCenter, text)
        else:
            rect = option.rect
            rect.adjust(0, 0, 0, 0)
            painter.rect = rect

            super(CustomItemDelegate, self).paint(painter, option, index)
