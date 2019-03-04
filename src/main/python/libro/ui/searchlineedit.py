from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QIcon

class SearchLineEdit(QLineEdit):
    def __init__(self, parent):
        super(SearchLineEdit, self).__init__(parent)
        self.setPlaceholderText('Search')
        self.setClearButtonEnabled(True)
        action = self.addAction(QIcon(':/icons/search-icon.png'), QLineEdit.LeadingPosition)
