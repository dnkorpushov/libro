import os
import sys
from PyQt5.QtWidgets import QDialog, QFileDialog
from libro.ui.settingsdialog_ui import Ui_Dialog
import libro.config as config


class SettingsDialog(QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)

        for f in ['epub', 'mobi', 'azw3']:
            self.formatCombo.addItem(f, f)

        self.converterPathEdit.setText(config.converter_path)
        self.configFileEdit.setText(config.converter_config)
        self.convertToFolderEdit.setText(config.convert_to_folder)
        self.formatCombo.setCurrentIndex(self.formatCombo.findData(config.output_format))

    def onConverterPathSelect(self):
        dlg = QFileDialog(self, 'Select fb2c executable')
        dlg.setFileMode(QFileDialog.ExistingFiles)
        if sys.platform == 'win32':
            dlg.setNameFilters(['fb2c.exe (fb2c.exe)', 'All files (*.*)'])
        else:
            dlg.setNameFilters(['fb2c (fb2c)', 'All files (*.*)'])
        if dlg.exec_():
            self.converterPathEdit.setText(os.path.normpath(dlg.selectedFiles()[0]))

    def onConfigPathSelect(self):
        dlg = QFileDialog(self, 'Select fb2c configuraton file')
        dlg.setFileMode(QFileDialog.ExistingFiles)
        dlg.setNameFilters(['Configuration files (*.toml *.json *.yaml)', 'All files (*.*)'])
        if dlg.exec_():
            self.configFileEdit.setText(os.path.normpath(dlg.selectedFiles()[0]))

    def onConvertToPathSelect(self):
        dlg = QFileDialog(self, 'Select destination folder')
        if config.convert_to_folder:
            dlg.setDirectory(config.convert_to_folder)
        dlg.setFileMode(QFileDialog.Directory)
        dlg.setOption(QFileDialog.ShowDirsOnly, True)

        if dlg.exec_():
            self.convertToFolderEdit.setText(os.path.normpath(dlg.selectedFiles()[0]))

    def accept(self):
        config.converter_path = self.converterPathEdit.text()
        config.converter_config = self.configFileEdit.text()
        config.convert_to_folder = self.convertToFolderEdit.text()
        config.output_format = self.formatCombo.currentData()
        super(SettingsDialog, self).accept()
