# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\main\designer\settingsdialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(450, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(450, 300))
        Dialog.setMaximumSize(QtCore.QSize(450, 300))
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setContentsMargins(6, 6, 6, 6)
        self.gridLayout_2.setSpacing(3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.converterPathEdit = QtWidgets.QLineEdit(self.groupBox)
        self.converterPathEdit.setObjectName("converterPathEdit")
        self.horizontalLayout.addWidget(self.converterPathEdit)
        self.converterPathButton = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.converterPathButton.sizePolicy().hasHeightForWidth())
        self.converterPathButton.setSizePolicy(sizePolicy)
        self.converterPathButton.setObjectName("converterPathButton")
        self.horizontalLayout.addWidget(self.converterPathButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.configFileEdit = QtWidgets.QLineEdit(self.groupBox)
        self.configFileEdit.setObjectName("configFileEdit")
        self.horizontalLayout_2.addWidget(self.configFileEdit)
        self.configFileButton = QtWidgets.QPushButton(self.groupBox)
        self.configFileButton.setObjectName("configFileButton")
        self.horizontalLayout_2.addWidget(self.configFileButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.convertToFolderEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.convertToFolderEdit.setObjectName("convertToFolderEdit")
        self.horizontalLayout_3.addWidget(self.convertToFolderEdit)
        self.convertToFolderButton = QtWidgets.QPushButton(self.groupBox_2)
        self.convertToFolderButton.setObjectName("convertToFolderButton")
        self.horizontalLayout_3.addWidget(self.convertToFolderButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.formatCombo = QtWidgets.QComboBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.formatCombo.sizePolicy().hasHeightForWidth())
        self.formatCombo.setSizePolicy(sizePolicy)
        self.formatCombo.setObjectName("formatCombo")
        self.verticalLayout.addWidget(self.formatCombo)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout_2.addWidget(self.groupBox_2, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 3, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.converterPathButton.clicked.connect(Dialog.onConverterPathSelect)
        self.convertToFolderButton.clicked.connect(Dialog.onConvertToPathSelect)
        self.configFileButton.clicked.connect(Dialog.onConfigPathSelect)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Settings"))
        self.groupBox.setTitle(_translate("Dialog", "fb2c converter settings"))
        self.label.setText(_translate("Dialog", "Path to fb2c converter executable"))
        self.converterPathButton.setText(_translate("Dialog", "Select"))
        self.label_2.setText(_translate("Dialog", "Path to fb2c custom configuration file (optional)"))
        self.configFileButton.setText(_translate("Dialog", "Select"))
        self.groupBox_2.setTitle(_translate("Dialog", "Output settings"))
        self.label_4.setText(_translate("Dialog", "Convert to folder (optional)"))
        self.convertToFolderButton.setText(_translate("Dialog", "Select"))
        self.label_3.setText(_translate("Dialog", "Output format:"))
