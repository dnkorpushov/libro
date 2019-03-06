import os

from PyQt5.QtWidgets import QDialog, QMenu, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QPoint, QByteArray, QBuffer, QEvent

from libro.ui.editdialog_ui import Ui_Dialog
import libro.utils.ui as uiUtils


class EditDialog(QDialog, Ui_Dialog):
    def __init__(self, parent, booksMeta):
        super(EditDialog, self).__init__(parent)
        self.setupUi(self)
        self.booksMeta = booksMeta

        for i in range(len(self.booksMeta)):
            self.authorEdit.addUserItem(self.booksMeta[i].get_author_string())
            self.titleEdit.addUserItem(self.booksMeta[i].title)
            self.seriesEdit.addUserItem(self.booksMeta[i].series)
            self.seriesIndexEdit.addUserItem(self.booksMeta[i].series_index)
            self.tagsEdit.addUserItem(self.booksMeta[i].get_tag_string())
            self.langEdit.addUserItem(self.booksMeta[i].lang)
            self.translatorEdit.addUserItem(self.booksMeta[i].get_translator_string(name_format='{#f {#m }}#l',
                                                                                    short=False))

        self.authorEdit.setInitialIndex()
        self.titleEdit.setInitialIndex()
        self.seriesEdit.setInitialIndex()
        self.seriesIndexEdit.setInitialIndex()
        self.tagsEdit.setInitialIndex()
        self.langEdit.setInitialIndex()
        self.translatorEdit.setInitialIndex()

        if len(self.booksMeta) == 1:
            self.setBookCover(self.booksMeta[0].cover_image_data)
            self.coverImage.setContextMenuPolicy(Qt.CustomContextMenu)
            self.coverImage.customContextMenuRequested[QPoint].connect(self.contextCoverMenu)
            self.coverImage.setAcceptDrops(True)
            self.coverImage.installEventFilter(self)

    def eventFilter(self, source, event):
        if source is self.coverImage:
            if event.type() == QEvent.DragEnter:
                if event.mimeData().hasUrls():
                    event.accept()
                    return True
                else:
                    event.ignore()
            elif event.type() == QEvent.Drop:
                fileList = [u.toLocalFile() for u in event.mimeData().urls()]
                for f in fileList:
                    self.loadCoverFromFile(f)
                    break
                event.accept()
                return True
        return QWidget.eventFilter(self, source, event)

    def setBookCover(self, image):
        if image is not None:
            pix = QPixmap()
            pix.loadFromData(image)
            scaled_pix = pix.scaled(150, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.coverImage.setPixmap(scaled_pix)

    def loadCoverFromFile(self, file):
        if os.path.exists(file):
            cover_pixmap = QPixmap()
            if cover_pixmap.load(file):
                data = QByteArray()
                buf = QBuffer(data)
                cover_pixmap.save(buf, 'JPG')
                self.booksMeta[0].cover_image_data = bytes(buf.buffer())
                self.booksMeta[0].cover_image_name = 'cover.jpg'
                self.setBookCover(self.booksMeta[0].cover_image_data)

    def saveCoverToFile(self, file):
        cover_pixmap = QPixmap()
        cover_pixmap.loadFromData(self.booksMeta[0].cover_image_data)
        cover_pixmap.save(file, os.path.splitext(file)[1][1:].upper())

    def contextCoverMenu(self, point):
        menu = QMenu()
        actionLoad = menu.addAction('Load from file...')
        actionSave = menu.addAction('Save to file...')
        actionClear = menu.addAction('Clear')

        action = menu.exec_(self.coverImage.mapToGlobal(point))

        if action == actionLoad:
            files = uiUtils.getFiles(self, title='Select cover file', fileExt='Image files (*.png *.jpg *.bmp)')
            if files is not None:
                self.loadCoverFromFile(files[0])

        elif action == actionSave:
            files = uiUtils.getFiles(self, title='Save cover image as',
                                     fileExt='Image files (*.png *.jpg *.bmp)', saveDialog=True)
            if files is not None:
                self.saveCoverToFile(files[0])

        elif action == actionClear:
            self.coverImage.clear()
            self.booksMeta[0].cover_image_data = None
            self.booksMeta[0].cover_image_name = ''

    def accept(self):
        for i in range(len(self.booksMeta)):
            self.booksMeta[i].set_author_from_string(self.authorEdit.getUserText(self.booksMeta[i].get_author_string()))
            self.booksMeta[i].title = self.titleEdit.getUserText(self.booksMeta[i].title)
            self.booksMeta[i].series = self.seriesEdit.getUserText(self.booksMeta[i].series)
            try:
                self.booksMeta[i].series_index = int(self.seriesIndexEdit.getUserText(self.booksMeta[i].series_index))
            except (ValueError, TypeError):
                self.booksMeta[i].series_index = None
            self.booksMeta[i].set_tag_from_string(self.tagsEdit.getUserText(self.booksMeta[i].get_tag_string()))
            self.booksMeta[i].lang = self.langEdit.getUserText(self.booksMeta[i].lang)
            self.booksMeta[i].set_translator_from_string(self.translatorEdit.getUserText(self.booksMeta[i].get_translator_string()))
        super(EditDialog, self).accept()

    def getBooksMeta(self):
        return self.booksMeta
