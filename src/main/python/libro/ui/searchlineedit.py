from PyQt5.QtWidgets import QLineEdit


class SearchLineEdit(QLineEdit):
    def __init__(self, parent):
        super(SearchLineEdit, self).__init__(parent)
        self.setPlaceholderText('Search')
        self.setClearButtonEnabled(True)
