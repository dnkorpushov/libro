from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, QCoreApplication
from libro.ui.processdialog_ui import Ui_ProcessDialog
import libro.library as library

_tr = QCoreApplication.translate


class Worker(QObject):
    currentProgress = pyqtSignal(int, int)
    finished = pyqtSignal()

    def __init__(self, books, parent=None):
        super(Worker, self).__init__(parent)
        self.books = books
        self.isRunning = True
        self.errors = []

    def addBooks(self):
        i = 0
        count = len(self.books)
        for book in self.books:
            if self.isRunning:
                i += 1
                src, err = library.add_book(book)
                if err:
                    self.errors.append({'src': src, 'dst': '', 'err': err})
                self.currentProgress.emit(i, count)
            else:
                break

        self.finished.emit()

    def kill(self):
        self.isRunning = False


class AddBooksDialog(QDialog, Ui_ProcessDialog):
    def __init__(self, parent, books):
        super(AddBooksDialog, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle(_tr('add', 'Add files'))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

        self.progress.setMaximum(len(books))
        self.progress.setMinimum(0)

        self.thread = QThread()
        self.worker = Worker(books)
        self.worker.currentProgress.connect(self.setCurrentProgress)
        self.worker.moveToThread(self.thread)
        self.worker.finished.connect(self.thread.quit)

        self.thread.started.connect(self.worker.addBooks)
        self.thread.finished.connect(self.close)

    def setCurrentProgress(self, current_index, count):
        self.label.setText(_tr('add', 'Processing {} of {}').format(current_index, count))
        self.progress.setValue(current_index)

    def cancelProcess(self):
        self.worker.kill()

    def showEvent(self, event):
        self.thread.start()
