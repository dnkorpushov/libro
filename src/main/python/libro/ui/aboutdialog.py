from PyQt5.QtWidgets import QDialog
from libro.ui.aboutdialog_ui import Ui_AboutDialog
import libro.version as version


class AboutDialog(QDialog, Ui_AboutDialog):
    def __init__(self, parent):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)
        self.labelVersion.setText(version.version)
