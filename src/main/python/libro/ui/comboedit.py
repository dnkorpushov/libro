from enum import Enum
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import QCoreApplication

_tr = QCoreApplication.translate


class ItemAction(Enum):
    Save = 0
    Clear = 1
    SaveUserData = 2


class ComboEdit(QComboBox):
    def __init__(self, parent):
        super(ComboEdit, self).__init__(parent)
        self.setEditable(True)
        self.addItem(_tr('edit', '< Save >'), ItemAction.Save)
        self.addItem(_tr('edit', '< Clear >'), ItemAction.Clear)

    def addUserItem(self, text):
        if self.findText(text) == -1:
            self.addItem(text, ItemAction.SaveUserData)

    def setInitialIndex(self):
        if self.count() == 3:
            self.setCurrentIndex(2)
        else:
            self.setCurrentIndex(0)

    def getUserText(self, userText):
        if self.currentData() == ItemAction.Save:
            return userText
        elif self.currentData() == ItemAction.Clear:
            return None
        else:
            return self.currentText()
