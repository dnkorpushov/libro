import os
import tempfile
import shutil
import webbrowser

from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox, QMenu
from PyQt5.QtCore import QEvent, Qt, QTimer, QCoreApplication
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
from libro.ui.logviewdialog import LogviewDialog
from libro.ui.collectiondialog import CollectionDialog
from libro.ui.smartcollectiondialog import SmartCollectionDialog

from libro.utils import util
from libro.utils import ui as uiUtils

_tr = QCoreApplication.translate

HELP_URL = 'https://github.com/dnkorpushov/libro/wiki'
SUPPORT_URL = 'http://4pda.ru/forum/index.php?showtopic=947577'


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, resources):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Libro')

        config.load()
        if not os.path.exists(config.config_dir):
            config.save()

        if config.is_library_mode:
            db_name = os.path.join(config.config_dir, 'libro.db')
            config.ui_display_sort_author = True
        else:
            db_name = ':memory:'
            config.ui_display_sort_author = False

        if not config.converter_config:
            for key in resources.keys():
                src = resources[key]
                dst = os.path.join(config.config_dir, os.path.split(src)[1])
                try:
                    shutil.copyfile(src, dst)
                    if key == 'default_config':
                        config.converter_config = dst
                        config.save()
                except Exception:
                    print(_tr('main', 'Error while copy file: {}').format(src))

        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(db_name)
        db.open()
        config.db = db

        if not library.is_created():
            library.create()
        library.update()

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

        if config.is_library_mode:
            self.navList.setVisible(True)
            # self.navList.setVisible(False)
            self.navList.addHeaderItem(_tr('main', 'Library'))
            self.navList.addItem(library.Collection(id=library.SystemCollectionId.AllBooks,
                                                    type=library.CollectionType.System,
                                                    name=_tr('main', 'All books')))
            self.navList.addItem(library.Collection(id=library.SystemCollectionId.AddedToday,
                                                    type=library.CollectionType.System,
                                                    name=_tr('main', 'Added today')))
            self.navList.addItem(library.Collection(id=library.SystemCollectionId.AddedLastWeek,
                                                    type=library.CollectionType.System,
                                                    name=_tr('main', 'Added last week')))
            self.navList.addHeaderItem(_tr('main', 'Collections'))

            collectionList = library.get_collection_list()
            for c in collectionList:
                self.navList.addItem(c)

        else:
            self.navList.setVisible(False)

        self.enableControls()

        self.deviceStatusTimer = QTimer()
        self.deviceStatusTimer.timeout.connect(self.checkDeviceStatus)
        self.deviceStatusTimer.start(1000)

    def checkDeviceStatus(self):
        if config.device_path:
            device_path = config.device_path
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
            if util.check_mail_setings(config.converter_config):
                self.actionSendBooksViaMail.setEnabled(True)
            else:
                self.actionSendBooksViaMail.setEnabled(False)
            if config.device_path:
                self.actionSendToReader.setEnabled(True)
            else:
                self.actionSendToReader.setEnabled(False)

        if config.is_library_mode and len(self.bookTable.selectionModel().selectedRows()) == 0:
            self.actionConvertToDisk.setEnabled(False)
            self.actionSendToReader.setEnabled(False)
            self.actionSendBooksViaMail.setEnabled(False)

    def searchBooks(self):
        self.bookTable.search(self.searchEdit.text())
        self.enableControls()

    def clearSearch(self):
        if len(self.searchEdit.text()) == 0:
            self.bookTable.search('')

    def onActionAddBooks(self):
        files = uiUtils.getFiles(self, title=_tr('main', 'Select files'), defaultPath=config.last_used_open_path,
                                 fileExt=_tr('main', 'Ebook files (*.fb2 *.fb2.zip *.zip *.epub)'), multipleSelect=True)
        if files is not None:
            config.last_used_open_path = os.path.split(files[0])[0]
            self.addFiles(files)

    def bookTableContextMenu(self, pos):
        if len(self.bookTable.selectionModel().selectedRows()) > 0:
            menu = QMenu()
            menu.addAction(self.actionEditMetadata)
            menu.addAction(self.actionRemoveBooks)
            if config.is_library_mode:
                sendMenu = QMenu(_tr('main', 'Send to...'))
                sendMenu.addAction(self.actionConvertToDisk)
                sendMenu.addAction(self.actionSendToReader)
                sendMenu.addAction(self.actionSendBooksViaMail)
                menu.addSeparator()
                menu.addMenu(sendMenu)
            menu.exec_(self.bookTable.viewport().mapToGlobal(pos))

    def onActionRemoveBooks(self):
        if config.is_library_mode:
            messageText = _tr('main', 'Remove selected files from library?')
        else:
            messageText = _tr('main', 'Remove selected files from list?')

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
        if len(dlg.worker.errors) > 0:
            logDlg = LogviewDialog(self, dlg.worker.errors, title=_tr('main', 'Loading errors'))
            logDlg.exec()

    def onActionSendToDevice(self):
        if config.device_path:
            self.runConvert(config.device_path, windowTitle=_tr('main', 'Send to reader device'))

    def onActionSendViaMail(self):
        temp_dir = tempfile.mkdtemp(prefix='lbr')
        if os.path.exists(temp_dir):
            self.runConvert(temp_dir, windowTitle=_tr('main', 'Send to mail'), sendToKindle=True)
        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass

    def onActionSendToFolder(self):
        dest_folder = uiUtils.getFolder(self, _tr('main', 'Select destination folder'),
                                        defaultPath=config.last_used_convert_path)
        if dest_folder is not None:
            config.last_used_convert_path = dest_folder
            self.runConvert(dest_folder, windowTitle=_tr('main', 'Send to folder'))

    def runConvert(self, destFolder, windowTitle, sendToKindle=False):
        if not config.converter_executable_path or not os.path.exists(config.converter_executable_path):
            QMessageBox.critical(self,
                                 'Libro',
                                 _tr('main',
                                     'Converter fb2converter not found!\nCheck settings for correct path.'))
        else:
            books_id = []
            util.set_converter_log_file(config.converter_config, config.converter_log_file)
            if config.is_library_mode:
                books_id = self.bookTable.getSelectedBooksId()
            else:
                books_id = self.bookTable.getBooksId()
            if len(books_id) > 0:
                convDlg = ConvertDialog(self, books_id, destFolder, sendToKindle)
                convDlg.exec()
                if len(convDlg.convertError) > 0:
                    logDlg = LogviewDialog(self, convDlg.convertError, title=_tr('main', 'Converson errors'))
                    logDlg.exec()

    def onActionNewCollection(self):
        dlg = CollectionDialog(self)
        if dlg.exec_():
            collection = dlg.collection
            collection, err = library.create_collection(collection)
            if not err:
                self.navList.addItem(collection)
            else:
                QMessageBox.critical(self, 'Libro', err)

    def onActionNewSmartCollection(self):
        dlg = SmartCollectionDialog(self)
        if dlg.exec_():
            collection = dlg.collection
            collection, err = library.create_collection(collection)
            if not err:
                self.navList.addItem(collection)
            else:
                QMessageBox.critical(self, 'Libro', err)

    def onActionEditCollection(self):
        pass

    def onActionDeleteCollection(self):
        pass

    def onActionSettings(self):
        dlg = PreferencesDialog(self)
        dlg.exec()
        if config.is_need_restart:
            config.is_need_restart = False
            QMessageBox.information(self, 'Libro', _tr('main', 'Restart Libro to apply changes.'))
        self.enableControls()

    def onActionAbout(self):
        dlg = AboutDialog(self)
        dlg.exec()

    def onActionAboutQt(self):
        QMessageBox.aboutQt(self)

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

    def onActionHelp(self):
        webbrowser.open(HELP_URL)

    def onActionSupportForum(self):
        webbrowser.open(SUPPORT_URL)

    def closeEvent(self, event):
        self.saveSettings()

    def saveSettings(self):
        config.ui_window_x = self.pos().x()
        config.ui_window_y = self.pos().y()
        config.ui_window_width = self.size().width()
        config.ui_window_height = self.size().height()
        if config.is_library_mode:
            config.ui_splitter_sizes = self.splitter.sizes()
        else:
            config.ui_splitter_sizes = []
        config.ui_columns_width = []
        for i in range(self.bookTable.model().columnCount()):
            config.ui_columns_width.append(self.bookTable.columnWidth(i))
        config.save()
