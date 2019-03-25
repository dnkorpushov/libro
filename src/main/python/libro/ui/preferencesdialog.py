import sys
import os
from PyQt5.QtWidgets import QDialog

from libro.ui.preferencesdialog_ui import Ui_Dialog

import libro.config as config
import libro.configdata as data
import libro.utils.ui as uiUtils


class PreferencesDialog(QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(PreferencesDialog, self).__init__(parent)
        self.setupUi(self)
        self.initValues()

    def initValues(self):
        for item in data.output_format:
            self.outputFormatCombo.addItem(item, item)

        self.libraryModeRadio.setChecked(config.is_library_mode)
        self.converterModeRadio.setChecked(not config.is_library_mode)
        self.collectFilesCheck.setChecked(config.collect_files)
        self.libraryRootEdit.setText(config.library_root_path)
        self.filenamePatternEdit.setCurrentText(config.filename_pattern)
        self.deviceMountpointEdit.setText(config.device_path)

        self.outputFormatCombo.setCurrentIndex(self.outputFormatCombo.findData(config.converter_output_format))
        self.converterPathEdit.setText(config.converter_executable_path)
        self.converterConfigEdit.setText(config.converter_config)

        self.onLibroModeSelect()
        self.onCollectFilesCheck()

    def onLibroModeSelect(self):
        self.libraryOptionsGroup.setEnabled(not self.converterModeRadio.isChecked())
        self.onCollectFilesCheck()

    def onLibraryRootSelect(self):
        path = uiUtils.getFolder(self, title='Select library root',
                                 defaultPath=self.libraryRootEdit.text())
        if path:
            self.libraryRootEdit.setText(path)

    def onDeviceMountpointSelect(self):
        path = uiUtils.getFolder(self, title='Select reader device mountpoint',
                                 defaultPath=self.deviceMountpointEdit.text())
        if path:
            self.deviceMountpointEdit.setText(path)

    def onConverterPathSelect(self):
        if sys.platform == 'win32':
            fileExt = 'fb2converter executable (fb2c.exe)'
        else:
            fileExt = 'fb2converter executable (fb2c)'
        if len(self.converterPathEdit.text()) > 0:
            defaultPath = os.path.split(self.converterPathEdit.text())[0]
        else:
            defaultPath = None
        files = uiUtils.getFiles(self, title='Select fb2converter executable', fileExt=fileExt, defaultPath=defaultPath)
        if files:
            self.converterPathEdit.setText(files[0])

    def onConfigFileSelect(self):
        fileExt = 'Converter configuration file (*.toml *.yaml *.json)'
        if len(self.converterConfigEdit.text()) > 0:
            defaultPath = os.path.split(self.converterConfigEdit.text())[0]
        else:
            defaultPath = None
        files = uiUtils.getFiles(self, title='Select converter configuration file',
                                 fileExt=fileExt, defaultPath=defaultPath)
        if files:
            self.converterConfigEdit.setText(files[0])

    def onCollectFilesCheck(self):
        self.libraryRootEdit.setEnabled(self.collectFilesCheck.isChecked())
        self.libraryRootSelectButton.setEnabled(self.collectFilesCheck.isChecked())
        self.filenamePatternEdit.setEnabled(self.collectFilesCheck.isChecked())

    def accept(self):
        if config.is_library_mode != self.libraryModeRadio.isChecked():
            config.is_need_restart = True

        config.is_library_mode = self.libraryModeRadio.isChecked()
        config.collect_files = self.collectFilesCheck.isChecked()
        config.library_root_path = self.libraryRootEdit.text()
        config.filename_pattern = self.filenamePatternEdit.currentText()
        config.device_path = self.deviceMountpointEdit.text()

        config.converter_output_format = self.outputFormatCombo.currentData()
        config.converter_executable_path = self.converterPathEdit.text()
        config.converter_config = self.converterConfigEdit.text()

        super(PreferencesDialog, self).accept()
