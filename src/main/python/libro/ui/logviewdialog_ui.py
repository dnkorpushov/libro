# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\main\designer\logviewdialog.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LogviewDialog(object):
    def setupUi(self, LogviewDialog):
        LogviewDialog.setObjectName("LogviewDialog")
        LogviewDialog.resize(599, 315)
        self.verticalLayout = QtWidgets.QVBoxLayout(LogviewDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(LogviewDialog)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.closeButton = QtWidgets.QPushButton(LogviewDialog)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(LogviewDialog)
        self.closeButton.clicked.connect(LogviewDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(LogviewDialog)

    def retranslateUi(self, LogviewDialog):
        _translate = QtCore.QCoreApplication.translate
        LogviewDialog.setWindowTitle(_translate("LogviewDialog", "View log"))
        self.closeButton.setText(_translate("LogviewDialog", "Close"))


