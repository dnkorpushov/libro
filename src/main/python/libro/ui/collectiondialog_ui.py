# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\main\designer\collectiondialog.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CollectionDialog(object):
    def setupUi(self, CollectionDialog):
        CollectionDialog.setObjectName("CollectionDialog")
        CollectionDialog.resize(330, 112)
        self.verticalLayout = QtWidgets.QVBoxLayout(CollectionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(CollectionDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.collectionNameEdit = QtWidgets.QLineEdit(CollectionDialog)
        self.collectionNameEdit.setObjectName("collectionNameEdit")
        self.verticalLayout.addWidget(self.collectionNameEdit)
        spacerItem = QtWidgets.QSpacerItem(20, 17, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(CollectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(CollectionDialog)
        self.buttonBox.accepted.connect(CollectionDialog.accept)
        self.buttonBox.rejected.connect(CollectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CollectionDialog)

    def retranslateUi(self, CollectionDialog):
        _translate = QtCore.QCoreApplication.translate
        CollectionDialog.setWindowTitle(_translate("CollectionDialog", "Dialog"))
        self.label.setText(_translate("CollectionDialog", "Collection name"))


