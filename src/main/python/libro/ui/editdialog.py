from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from libro.ui.editdialog_ui import Ui_Dialog


class EditDialog(QDialog, Ui_Dialog):
    def __init__(self, parent, booksInfo):
        super(EditDialog, self).__init__(parent)
        self.setupUi(self)
        self.booksInfo = booksInfo

        for i in range(len(self.booksInfo)):
            self.authorEdit.addUserItem(self.booksInfo[i].author)
            self.titleEdit.addUserItem(self.booksInfo[i].title)
            self.seriesEdit.addUserItem(self.booksInfo[i].series)
            self.seriesIndexEdit.addUserItem(str(self.booksInfo[i].series_index))
            self.tagsEdit.addUserItem(self.booksInfo[i].tags)
            self.langEdit.addUserItem(self.booksInfo[i].lang)
            self.translatorEdit.addUserItem(self.booksInfo[i].translator)

        self.authorEdit.setInitialIndex()
        self.titleEdit.setInitialIndex()
        self.seriesEdit.setInitialIndex()
        self.seriesIndexEdit.setInitialIndex()
        self.tagsEdit.setInitialIndex()
        self.langEdit.setInitialIndex()
        self.translatorEdit.setInitialIndex()

        if len(self.booksInfo) == 1:
            self.setBookCover(self.booksInfo[0].cover_image)

    def setBookCover(self, image):
        pix = QPixmap()
        pix.loadFromData(image)
        scaled_pix = pix.scaled(150, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.coverImage.setPixmap(scaled_pix)

    def accept(self):
        for i in range(len(self.booksInfo)):
            self.booksInfo[i].author = self.authorEdit.getUserText(self.booksInfo[i].author)
            self.booksInfo[i].title = self.titleEdit.getUserText(self.booksInfo[i].title)
            self.booksInfo[i].series = self.seriesEdit.getUserText(self.booksInfo[i].series)
            try:
                self.booksInfo[i].series_index = int(self.seriesIndexEdit.getUserText(self.booksInfo[i].series_index))
            except (ValueError, TypeError):
                self.booksInfo[i].series_index = None
            self.booksInfo[i].tags = self.tagsEdit.getUserText(self.booksInfo[i].tags)
            self.booksInfo[i].lang = self.langEdit.getUserText(self.booksInfo[i].lang)
            self.booksInfo[i].translator = self.translatorEdit.getUserText(self.booksInfo[i].translator)
        super(EditDialog, self).accept()

    def getBooksInfo(self):
        return self.booksInfo
