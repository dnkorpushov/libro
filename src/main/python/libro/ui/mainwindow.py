import os
import tempfile
import shutil

from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox, QMenu
from PyQt5.QtCore import QEvent, Qt, QTimer
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
        self.bookTable.selectionModel().selectionChanged.connect(self.enableControls)

        self.searchEdit = SearchLineEdit(self)
        self.searchEdit.returnPressed.connect(self.searchBooks)
        self.searchEdit.textChanged.connect(self.clearSearch)

        self.toolBar.addAction(self.actionAddBooks)
        self.toolBar.addAction(self.actionEditMetadata)
        self.toolBar.addAction(self.actionRemoveBooks)
        self.toolBar.addSpacer(15)
        self.toolBar.addAction(self.actionConvertToDisk)
        self.toolBar.addAction(self.actionSendToReader)
        self.toolBar.addAction(self.actionSendBooksViaMail)
        self.toolBar.addSpacer(15)
        self.toolBar.addAction(self.actionSettings)
        self.toolBar.addExpandedSpacer()
        self.searchAction = self.toolBar.addWidget(self.searchEdit)
        self.toolBar.addSpacer(10)

        if config.ui_window_width:
            self.resize(config.ui_window_width, config.ui_window_height)
            self.move(config.ui_window_x, config.ui_window_y)

        self.navTree.setVisible(config.libro_is_library_mode)
        self.enableControls()

        self.deviceStatusTimer = QTimer()
        self.deviceStatusTimer.timeout.connect(self.checkDeviceStatus)
        self.deviceStatusTimer.start(1000)

    def checkDeviceStatus(self):
        if config.libro_device_path:
            device_path = config.libro_device_path
        else:
            device_path = util.find_reader_device()

        if os.path.exists(device_path):
            config.device_path = device_path
        else:
            config.device_path = ''
        self.enableControls()

    def enableControls(self):
        if len(self.bookTable.selectionModel().selectedRows()) > 0:
            self.actionEditMetadata.setEnabled(True)
            self.actionRemoveBooks.setEnabled(True)
        else:
            self.actionEditMetadata.setEnabled(False)
            self.actionRemoveBooks.setEnabled(False)

        if self.bookTable.model().rowCount() == 0:
            self.actionConvertToDisk.setEnabled(False)
            self.actionSendToReader.setEnabled(False)
            self.actionSendBooksViaMail.setEnabled(False)
        else:
            self.actionConvertToDisk.setEnabled(True)
            if config.check_mail_settings():
                self.actionSendBooksViaMail.setEnabled(True)
            else:
                self.actionSendBooksViaMail.setEnabled(False)
            if config.device_path:
                self.actionSendToReader.setEnabled(True)
            else:
                self.actionSendToReader.setEnabled(False)

    def searchBooks(self):
        self.bookTable.search(self.searchEdit.text())
        self.enableControls()

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
        self.enableControls()

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
        self.enableControls()

    def onActionSendToDevice(self):
        if config.device_path:
            self.runConvert(config.device_path, windowTitle='Send to device')

    def onActionSendViaMail(self):
        temp_dir = tempfile.mkdtemp(prefix='lbr')
        if os.path.exists(temp_dir):
            self.runConvert(temp_dir, windowTitle='Send via mail', sendToKindle=True)
        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass

    def onActionSendToFolder(self):
        if not config.fb2c_convert_to_folder:
            dest_folder = uiUtils.getFolder(self, 'Select destination folder',
                                            defaultPath=config.last_used_convert_path)
            if dest_folder is not None:
                config.last_used_convert_path = dest_folder
        else:
            dest_folder = config.fb2c_convert_to_folder

        if dest_folder:
            self.runConvert(dest_folder, windowTitle='Convert to folder')

    def runConvert(self, destFolder, windowTitle, sendToKindle=False):
        if not config.fb2c_executable_path or not os.path.exists(config.fb2c_executable_path):
            QMessageBox.critical(self,
                                 'Libro',
                                 'Converter fb2c not found!\nCheck settings for correct converter path.')
        else:
            books_id = self.bookTable.getBooksId()
            convDlg = ConvertDialog(self, books_id, destFolder, sendToKindle)
            convDlg.exec()

    def onActionSettings(self):
        dlg = PreferencesDialog(self)
        dlg.exec()
        if config.is_need_restart:
            config.is_need_restart = False
            QMessageBox.information(self, 'Libro', 'Restart Libro to apply changes.')
        self.enableControls()

    def onActionAbout(self):
        dlg = AboutDialog(self)
        dlg.exec()

    def onActionAboutQt(self):
        QMessageBox.aboutQt(self)

    def onActionViewLog(self):
        dlg = LogviewDialog(self, file=config.converter_log_file)
        dlg.exec()

    def onActionEditMetadata(self):
        booksMeta = []
        booksId = self.bookTable.getSelectedBooksId()
        if len(booksId) > 0:
            for bookId in booksId:
                bookMeta = library.get_book_info(bookId)
                booksMeta.append(bookMeta)

            dlg = EditDialog(self, booksMeta=booksMeta)
            if dlg.exec():
                booksMeta = dlg.getBooksMeta()
                for bookMeta in booksMeta:
                    library.update_book_info(bookMeta)
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
