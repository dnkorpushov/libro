from PyQt5.QtWidgets import QDialog, QTextEdit
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtCore import QCoreApplication

from libro.ui.logviewdialog_ui import Ui_LogviewDialog

_tr = QCoreApplication.translate


class LogviewDialog(QDialog, Ui_LogviewDialog):
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
            self.textEdit.append(_tr('log', '<b>File:</b> {}').format(rec['src']))
            for msg in rec['err']:
                if msg[0] == 'ERROR':
                    self.textEdit.append(_tr('log', '<b>Error:</b> {}').format(msg[1]))
                elif msg[0] == 'WARN':
                    self.textEdit.append(_tr('log', '<b>Warning:</b> {}').format(msg[1]))
            self.textEdit.append(' ')
