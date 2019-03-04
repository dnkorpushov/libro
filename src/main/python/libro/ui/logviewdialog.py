import os
import codecs
from PyQt5.QtWidgets import QDialog, QTextEdit
from PyQt5.QtGui import QFontDatabase

from libro.ui.logviewdialog_ui import Ui_Dialog


class LogviewDialog(QDialog, Ui_Dialog):
    def __init__(self, parent, file):
        super(LogviewDialog, self).__init__(parent)
        self.setupUi(self)
        self.textEdit.setAcceptRichText(True)
        self.textEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.file = file

        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.textEdit.setFont(font)

        self.loadFile()

    def loadFile(self):
        if os.path.exists(self.file):
            with codecs.open(self.file, mode='r', encoding='utf-8') as f:
                for line in f:
                    self.textEdit.append(self._formatLine(line))

    def _formatLine(self, line):
        line = line.strip()
        fields = line.split('\t')

        if fields[1].lower() == 'info':
            return '<font color="#006600">{}</font>'.format(line)
        elif fields[1].lower() == 'warn':
            return '<font color="#CC3300">{}</font>'.format(line)
        elif fields[1].lower() == 'error':
            return '<font color="#660000">{}</font>'.format(line)

        return line

