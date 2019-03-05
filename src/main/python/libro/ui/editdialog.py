from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from libro.ui.editdialog_ui import Ui_Dialog


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

    def setBookCover(self, image):
        pix = QPixmap()
        pix.loadFromData(image)
        scaled_pix = pix.scaled(150, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.coverImage.setPixmap(scaled_pix)

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
