from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QProcess
from libro.ui.processdialog_ui import Ui_Dialog
import libro.config as config
import libro.library as library


class ConvertDialog(QDialog, Ui_Dialog):
    def __init__(self, parent, books_id, dest_folder):
        super(ConvertDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Convert books')
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

        self.books_id = books_id
        self.dest_folder = dest_folder

        self.process = QProcess(self)
        self.process.finished.connect(self.endProcess)
        self.count = len(self.books_id)
        self.current_index = 0
        self.canceled = False

        self.progress.setMaximum(self.count)
        self.progress.setMinimum(0)

    def setCurrentProgress(self):
        self.label.setText('Processing {} of {}'.format(self.current_index, self.count))
        self.progress.setValue(self.current_index)

    def runConvert(self):
        self.setCurrentProgress()
        if self.current_index < self.count and not self.canceled:
            book_info = library.get_book_info(self.books_id[self.current_index])
            args = []
            if book_info.type == 'epub' and config.output_format == 'epub':
                self.current_index += 1
                self.runConvert()
            else:
                if config.converter_config:
                    args.append('--config')
                    args.append(config.converter_config)
                if book_info.type == 'fb2':
                    args.append('convert')
                elif book_info.type == 'epub':
                    args.append('transfer')
                args.append('--to')
                args.append(config.output_format)
                args.append('--ow')
                args.append(book_info.file)
                args.append(self.dest_folder)
                self.process.start(config.converter_path, args)
        else:
            self.close()

    def cancelProcess(self):
        self.process.kill()
        self.canceled = True

    def endProcess(self, exitCode, exitStatus):
        self.current_index += 1
        self.runConvert()

    def showEvent(self, event):
        self.runConvert()

    def open(self):
        if self.count > 0:
            super(ConvertDialog, self).open()
