# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\main\designer\smartcollectiondialog.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SmartCollectionDialog(object):
    def setupUi(self, SmartCollectionDialog):
        SmartCollectionDialog.setObjectName("SmartCollectionDialog")
        SmartCollectionDialog.resize(373, 240)
        self.verticalLayout = QtWidgets.QVBoxLayout(SmartCollectionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(SmartCollectionDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.collectionNameEdit = QtWidgets.QLineEdit(SmartCollectionDialog)
        self.collectionNameEdit.setObjectName("collectionNameEdit")
        self.verticalLayout.addWidget(self.collectionNameEdit)
        self.label_2 = QtWidgets.QLabel(SmartCollectionDialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.criteriaEdit = QtWidgets.QTextEdit(SmartCollectionDialog)
        self.criteriaEdit.setObjectName("criteriaEdit")
        self.verticalLayout.addWidget(self.criteriaEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(SmartCollectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SmartCollectionDialog)
        self.buttonBox.accepted.connect(SmartCollectionDialog.accept)
        self.buttonBox.rejected.connect(SmartCollectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SmartCollectionDialog)

    def retranslateUi(self, SmartCollectionDialog):
        _translate = QtCore.QCoreApplication.translate
        SmartCollectionDialog.setWindowTitle(_translate("SmartCollectionDialog", "Dialog"))
        self.label.setText(_translate("SmartCollectionDialog", "Collection name"))
        self.label_2.setText(_translate("SmartCollectionDialog", "Search criteria"))


