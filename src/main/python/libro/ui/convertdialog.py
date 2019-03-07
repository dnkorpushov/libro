import shutil

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QProcess
from libro.ui.processdialog_ui import Ui_Dialog
import libro.config as config
import libro.converterconfig as converterconfig
import libro.library as library


class ConvertDialog(QDialog, Ui_Dialog):
    def __init__(self, parent, booksId, destFolder, sendToKindle):
        super(ConvertDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Convert books')
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

        self.booksId = booksId
        self.destFolder = destFolder
        self.sendToKindle = sendToKindle

        self.process = QProcess(self)
        self.process.finished.connect(self.endProcess)

        self.count = len(self.booksId)
        self.currentIndex = 0
        self.canceled = False

        self.progress.setMaximum(self.count)
        self.progress.setMinimum(0)

        self.setCurrentProgress()

    def setCurrentProgress(self):
        self.label.setText('Processing {} of {}'.format(self.currentIndex, self.count))
        self.progress.setValue(self.currentIndex)

    def runProcess(self):
        bookInfo = library.get_book_info(self.booksId[self.currentIndex])
        if bookInfo.book_format == 'epub' and config.fb2c_output_format == 'epub':
            try:
                shutil.copyfile(bookInfo, self.destFolder)
            except IOError:
                pass
            self.endConvertProcess(0, 0)
        else:
            args = []
            args.append('--config')
            if config.fb2c_is_custom_config and config.fb2c_custom_config:
                args.append(config.fb2c_custom_config)
            else:
                converterconfig.generate()
                args.append(config.default_converter_config)
            if bookInfo.book_format == 'fb2':
                args.append('convert')
            elif bookInfo.type == 'epub':
                args.append('transfer')
            args.append('--to')
            args.append(config.fb2c_output_format)
            if self.sendToKindle:
                args.append('--stk')
            args.append('--ow')
            args.append(bookInfo.file)
            args.append(self.destFolder)
            self.process.start(config.fb2c_executable_path, args)

    def cancelProcess(self):
        self.process.kill()
        self.canceled = True

    def endProcess(self, exitCode, exitStatus):
        self.currentIndex += 1
        self.setCurrentProgress()

        if self.currentIndex < self.count and not self.canceled:
            self.runProcess()
        else:
            self.close()

    def showEvent(self, event):
        self.runProcess()

    def open(self):
        if self.count > 0:
            super(ConvertDialog, self).open()
