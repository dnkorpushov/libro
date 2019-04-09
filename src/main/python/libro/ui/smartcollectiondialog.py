from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QCoreApplication

from libro.ui.smartcollectiondialog_ui import Ui_SmartCollectionDialog
from libro.library import Collection, CollectionType

_tr = QCoreApplication.translate


class SmartCollectionDialog(QDialog, Ui_SmartCollectionDialog):
    def __init__(self, parent=None, collection=None):
        super(SmartCollectionDialog, self).__init__(parent)
        self.setupUi(self)
        if collection is None:
            self.setWindowTitle(_tr('coll', 'New smart collection'))
            collection = Collection()
            collection.type = CollectionType.Smart
        else:
            self.setWindowTitle(_tr('coll', 'Edit smart collection'))
        self.collection = collection
        self.collectionNameEdit.setText(self.collection.name)
        self.criteriaEdit.setText(self.collection.criteria)

    def accept(self):
        self.collection.name = self.collectionNameEdit.text()
        self.collection.criteria = self.criteriaEdit.toPlainText()
        super(SmartCollectionDialog, self).accept()
