import os

from PyQt5.QtWidgets import QMainWindow, QWidget, QSizePolicy, QMessageBox, QMenu
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtSql import QSqlDatabase

import libro.config as config
import libro.library as library
import libro.converterconfig as converterconfig
from libro.ui.mainwindow_ui import Ui_MainWindow
from libro.ui.convertdialog import ConvertDialog
from libro.ui.addbooksdialog import AddBooksDialog
from libro.ui.preferencesdialog import PreferencesDialog
from libro.ui.aboutdialog import AboutDialog
from libro.ui.searchlineedit import SearchLineEdit
from libro.ui.editdialog import EditDialog
from libro.ui.logviewdialog import LogviewDialog

from libro.utils import util
from libro.utils import ui as uiUtils


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Libro')

        config.load()
        if not os.path.exists(config.config_dir):
            config.save()

        if config.libro_is_library_mode:
            db_name = os.path.join(config.config_dir, 'libro.db')
        else:
            db_name = ':memory:'

        if not os.path.exists(config.default_converter_config):
            converterconfig.generate_default()

        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(db_name)
        db.open()
        config.db = db

        if not library.is_created():
            library.create()

        self.bookTable.init(db=config.db, columnsWidth=config.ui_columns_width)
        self.bookTable.setContextMenuPolicy(Qt.CustomContextMenu)
        self.bookTable.customContextMenuRequested.connect(self.bookTableContextMenu)
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

        if config.ui_window_width:
            self.resize(config.ui_window_width, config.ui_window_height)
            self.move(config.ui_window_x, config.ui_window_y)

        self.navTree.setVisible(config.libro_is_library_mode)
        self.searchAction.setVisible(config.libro_is_library_mode)

    def searchBooks(self):
        self.bookTable.search(self.searchEdit.text())

    def clearSearch(self):
        if len(self.searchEdit.text()) == 0:
            self.bookTable.search('')

    def onActionAddBooks(self):
        files = uiUtils.getFiles(self, title='Select files', defaultPath=config.last_used_open_path,
                                 fileExt='Ebook files (*.fb2 *.fb2.zip *.zip *.epub)', multipleSelect=True)
        if files is not None:
            config.last_used_open_path = os.path.split(files[0])[0]
            self.addFiles(files)

    def bookTableContextMenu(self, pos):
        if len(self.bookTable.selectionModel().selectedRows()) > 0:
            menu = QMenu()
            menu.addAction(self.actionEditMetadata)
            menu.addAction(self.actionRemoveBooks)
            menu.exec_(self.bookTable.viewport().mapToGlobal(pos))

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
        if not config.fb2c_executable_path or not os.path.exists(config.fb2c_executable_path):
            QMessageBox.critical(self,
                                 'Libro',
                                 'Converter fb2c not found! \nCheck settings for correct converter path.')
        else:
            books_id = self.bookTable.getBooksId()
            dest_folder = None
            if len(books_id) > 0:
                if not config.fb2c_convert_to_folder:
                    dest_folder = uiUtils.getFolder(self, 'Select destination folder',
                                                    defaultPath=config.last_used_convert_path)
                    if dest_folder is not None:
                        config.last_used_convert_path = dest_folder
                else:
                    dest_folder = config.fb2c_convert_to_folder

                if dest_folder:
                    convDlg = ConvertDialog(self, books_id, dest_folder)
                    convDlg.exec()

    def onActionSettings(self):
        dlg = PreferencesDialog(self)
        dlg.exec()
        if config.is_need_restart:
            config.is_need_restart = False
            QMessageBox.information(self, 'Libro', 'Restart Libro to apply changes.')

    def onActionAbout(self):
        dlg = AboutDialog(self)
        dlg.exec()

    def onActionAboutQt(self):
        QMessageBox.aboutQt(self)

    def onActionViewLog(self):
        dlg = LogviewDialog(self, file=config.converter_log_file)
        dlg.exec()

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
        self.saveSettings()

    def saveSettings(self):
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
