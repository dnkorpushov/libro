import os
import codecs
from PyQt5.QtWidgets import QDialog, QTextEdit

from libro.ui.logviewdialog_ui import Ui_Dialog


class LogviewDialog(QDialog, Ui_Dialog):
    def __init__(self, parent, file):
        super(LogviewDialog, self).__init__(parent)
        self.setupUi(self)
        self.textEdit.setAcceptRichText(True)
        self.textEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.textEdit.setFontFamily('Consolas')
        self.file = file

        self.loadFile()

    def loadFile(self):
        if os.path.exists(self.file):
            with codecs.open(self.file, mode='r', encoding='utf-8') as f:
                for line in f:
                    self.textEdit.append('<p>{}</p>'.format(line))
