import os

from PyQt5.QtWidgets import QMainWindow, QWidget, QFileDialog, QSizePolicy, QMessageBox
from PyQt5.QtCore import QEvent
from PyQt5.QtSql import QSqlDatabase

import libro.config as config
import libro.library as library
from libro.ui.mainwindow_ui import Ui_MainWindow
from libro.ui.convertdialog import ConvertDialog
from libro.ui.addbooksdialog import AddBooksDialog
from libro.ui.preferencesdialog import PreferencesDialog
from libro.ui.aboutdialog import AboutDialog
from libro.ui.searchlineedit import SearchLineEdit
from libro.ui.editdialog import EditDialog
from libro.utils import util


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Libro')
        config.load()

        if config.libro_is_library_mode:
            db_name = os.path.join(config.config_dir, 'libro.db')
        else:
            db_name = ':memory:'

        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(db_name)
        db.open()
        config.db = db

        if not library.is_created():
            library.create()

        self.bookTable.init(db=config.db, columnsWidth=config.ui_columns_width)
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)

        if len(config.ui_splitter_sizes) > 0:
                self.splitter.setSizes(config.ui_splitter_sizes)

        self.bookTable.setAcceptDrops(True)
        self.bookTable.installEventFilter(self)

        self.searchEdit = SearchLineEdit(self)
        self.searchEdit.returnPressed.connect(self.searchBooks)
        self.searchEdit.textChanged.connect(self.clearSearch)

        sw = QWidget()
        sw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        pw = QWidget()
        pw.setFixedWidth(5)
        pw.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

        self.toolBar.addWidget(sw)
        self.searchAction = self.toolBar.addWidget(self.searchEdit)
        self.toolBar.addWidget(pw)

        # Restore settings
        if config.ui_window_width:
            self.resize(config.ui_window_width, config.ui_window_height)
            self.move(config.ui_window_x, config.ui_window_y)

        if not config.libro_is_library_mode:
            self.navTree.setVisible(False)
            self.searchAction.setVisible(False)

    def searchBooks(self):
        self.bookTable.search(self.searchEdit.text())

    def clearSearch(self):
        if len(self.searchEdit.text()) == 0:
            self.bookTable.search('')

    def onActionAddBooks(self):
        dlg = QFileDialog(self, 'Select files')
        if config.last_used_open_path:
            dlg.setDirectory(config.last_used_open_path)
        dlg.setFileMode(QFileDialog.ExistingFiles)
        dlg.setNameFilters(['Ebook files (*.fb2 *.fb2.zip *.zip *.epub)', 'All files (*.*)'])

        if dlg.exec_():
            config.last_used_open_path = os.path.split(dlg.selectedFiles()[0])[0]
            self.addFiles(dlg.selectedFiles())

    def onActionRemoveBooks(self):
        if config.libro_is_library_mode:
            messageText = 'Remove selected books from library?'
        else:
            messageText = 'Remove selected books from list?'

        if QMessageBox.question(self, 'Libro', messageText) == QMessageBox.Yes:
            booksId = self.bookTable.getSelectedBooksId()
            for bookId in booksId:
                library.delete_book(bookId)
            self.bookTable.model().select()

    def eventFilter(self, source, event):
        if source is self.bookTable:
            if event.type() == QEvent.DragEnter:
                if event.mimeData().hasUrls():
                    event.accept()
                    return True
                else:
                    event.ignore()
            elif event.type() == QEvent.Drop:
                urlList = [x.toLocalFile() for x in event.mimeData().urls()]
                self.addDropFilesAndDirs(urlList)
                event.accept()
                return True

        return QWidget.eventFilter(self, source, event)

    def addDropFilesAndDirs(self, urlList):
        fileList = []
        for item in urlList:
            if os.path.isdir(item):
                for root, dirs, files in os.walk(item):
                    for f in files:
                        if util.is_supported_format(f):
                            fileList.append(os.path.join(root, f))
            else:
                if util.is_supported_format(item):
                    fileList.append(item)
        self.addFiles(fileList)

    def addFiles(self, files):
        dlg = AddBooksDialog(self, files)
        dlg.exec()
        self.bookTable.model().select()

    def onActionConvertToDisk(self):
        if not config.converter_path or not os.path.exists(config.converter_path):
            QMessageBox.critical(self,
                                 'Libro for Kindle',
                                 'Converter fb2c not found! \nCheck settings for correct converter path.')
        else:
            books_id = self.bookTable.getBooksId()
            dest_folder = None
            if len(books_id) > 0:
                if not config.convert_to_folder:
                    dlg = QFileDialog(self, 'Select destination folder')
                    if config.last_used_convert_path:
                        dlg.setDirectory(config.last_used_convert_path)
                    dlg.setFileMode(QFileDialog.Directory)
                    dlg.setOption(QFileDialog.ShowDirsOnly, True)

                    if dlg.exec_():
                        config.last_used_convert_path = os.path.normpath(dlg.selectedFiles()[0])
                        dest_folder = config.last_used_convert_path
                else:
                    dest_folder = config.convert_to_folder

                if dest_folder:
                    convDlg = ConvertDialog(self, books_id, dest_folder)
                    convDlg.exec()

    def onActionSettings(self):
        dlg = PreferencesDialog(self)
        dlg.exec_()

    def onActionAbout(self):
        dlg = AboutDialog(self)
        dlg.exec()

    def onActionAboutQt(self):
        QMessageBox.aboutQt(self)

    def onActionEditMetadata(self):
        booksInfo = []
        booksId = self.bookTable.getSelectedBooksId()
        if len(booksId) > 0:
            for bookId in booksId:
                bookInfo = library.get_book_info(bookId)
                booksInfo.append(bookInfo)

            dlg = EditDialog(self, booksInfo=booksInfo)
            if dlg.exec():
                booksInfo = dlg.getBooksInfo()
                for book in booksInfo:
                    library.update_book_info(book)
                self.bookTable.updateSelectedRows()

    def closeEvent(self, event):
        config.ui_window_x = self.pos().x()
        config.ui_window_y = self.pos().y()
        config.ui_window_width = self.size().width()
        config.ui_window_height = self.size().height()
        if config.libro_is_library_mode:
            config.ui_splitter_sizes = self.splitter.sizes()
        else:
            config.ui_splitter_sizes = []
        config.ui_columns_width = []
        for i in range(self.bookTable.model().columnCount()):
            config.ui_columns_width.append(self.bookTable.columnWidth(i))
        config.save()
