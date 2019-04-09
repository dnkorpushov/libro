from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QCoreApplication

from libro.ui.collectiondialog_ui import Ui_CollectionDialog
from libro.library import Collection, CollectionType

_tr = QCoreApplication.translate


class CollectionDialog(QDialog, Ui_CollectionDialog):
    def __init__(self, parent=None, collection=None):
        super(CollectionDialog, self).__init__(parent)
        self.setupUi(self)
        if collection is None:
            self.setWindowTitle(_tr('coll', 'New collection'))
            collection = Collection()
            collection.type = CollectionType.Collection
        else:
            self.setWindowTitle(_tr('coll', 'Edit collection'))
        self.collection = collection
        self.collectionNameEdit.setText(self.collection.name)

    def accept(self):
        self.collection.name = self.collectionNameEdit.text()
        super(CollectionDialog, self).accept()
