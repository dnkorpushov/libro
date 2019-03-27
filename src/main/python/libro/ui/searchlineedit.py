from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication

_tr = QCoreApplication.translate


class SearchLineEdit(QLineEdit):
    def __init__(self, parent):
        super(SearchLineEdit, self).__init__(parent)
        self.setPlaceholderText(_tr('search', 'Search'))
        self.setClearButtonEnabled(True)
        action = self.addAction(QIcon(':/icons/search-icon.png'), QLineEdit.LeadingPosition)
