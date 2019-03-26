import os
import codecs
from PyQt5.QtWidgets import QDialog, QTextEdit
from PyQt5.QtGui import QFontDatabase

from libro.ui.logviewdialog_ui import Ui_Dialog


class LogviewDialog(QDialog, Ui_Dialog):
    def __init__(self, parent, log=[], title=None):
        super(LogviewDialog, self).__init__(parent)
        self.setupUi(self)
        self.textEdit.setAcceptRichText(True)
        self.textEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.log = log

        if title is not None:
            self.setWindowTitle(title)

        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.textEdit.setFont(font)

        self.loadLog()

    def loadLog(self):
        for rec in self.log:
            self.textEdit.append('<b>File:</b> {}'.format(rec['src']))
            self.textEdit.append('<b>Error:</b> {}'.format(rec['err']))
            self.textEdit.append(' ')
