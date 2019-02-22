from PyQt5.QtWidgets import QDialog
from libro.ui.aboutdialog_ui import Ui_Dialog


class AboutDialog(QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)
