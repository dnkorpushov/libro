# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\main\designer\processdialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProcessDialog(object):
    def setupUi(self, ProcessDialog):
        ProcessDialog.setObjectName("ProcessDialog")
        ProcessDialog.resize(350, 115)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ProcessDialog.sizePolicy().hasHeightForWidth())
        ProcessDialog.setSizePolicy(sizePolicy)
        ProcessDialog.setMinimumSize(QtCore.QSize(350, 115))
        ProcessDialog.setMaximumSize(QtCore.QSize(350, 115))
        self.gridLayout = QtWidgets.QGridLayout(ProcessDialog)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(ProcessDialog)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.progress = QtWidgets.QProgressBar(ProcessDialog)
        self.progress.setProperty("value", 0)
        self.progress.setTextVisible(False)
        self.progress.setObjectName("progress")
        self.verticalLayout.addWidget(self.progress)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cancelButton = QtWidgets.QPushButton(ProcessDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(ProcessDialog)
        self.cancelButton.clicked.connect(ProcessDialog.cancelProcess)
        QtCore.QMetaObject.connectSlotsByName(ProcessDialog)

    def retranslateUi(self, ProcessDialog):
        _translate = QtCore.QCoreApplication.translate
        ProcessDialog.setWindowTitle(_translate("ProcessDialog", "Converting books"))
        self.label.setText(_translate("ProcessDialog", "TextLabel"))
        self.cancelButton.setText(_translate("ProcessDialog", "Cancel"))

