import sys
import os
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtCore import QSize

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
        for item in data.notes_type:
            self.notesModeCombo.addItem(item, item)
        for item in data.apnx_type:
            self.apnxStyleCombo.addItem(item, item)
        for item in data.log_level:
            self.logLevelCombo.addItem(item, item)
        for item in data.log_mode:
            self.logModeCombo.addItem(item, item)
        for item in data.author_format:
            self.authorFormatEdit.addItem(item)
        for item in data.title_format:
            self.titleFormatEdit.addItem(item)

        self.libraryModeRadio.setChecked(config.libro_is_library_mode)
        self.converterModeRadio.setChecked(not config.libro_is_library_mode)
        self.collectFilesCheck.setChecked(config.libro_collect_files)
        self.libraryRootEdit.setText(config.libro_library_root_path)
        self.filenamePatternEdit.setCurrentText(config.libro_filename_pattern)

        self.useCustomConfigRadio.setChecked(config.fb2c_is_custom_config)
        self.useDefaultConfigRadio.setChecked(not config.fb2c_is_custom_config)
        self.outputFormatCombo.setCurrentIndex(self.outputFormatCombo.findData(config.fb2c_output_format))
        self.convertToFolderEdit.setText(config.fb2c_convert_to_folder)
        self.converterPathEdit.setText(config.fb2c_executable_path)
        self.configFileEdit.setText(config.fb2c_custom_config)
        self.stylesheetFileEdit.setText(config.fb2c_css_file)
        self.insertHyphenCheck.setChecked(config.fb2c_insert_soft_hyphen)
        self.notesModeCombo.setCurrentIndex(self.notesModeCombo.findData(config.fb2c_notes_mode))
        self.apnxStyleCombo.setCurrentIndex(self.apnxStyleCombo.findData(config.fb2c_apnx_mode))
        self.titleFormatEdit.setCurrentText(config.fb2c_title_format)
        self.authorFormatEdit.setCurrentText(config.fb2c_author_format)

        self.serverEdit.setText(config.fb2c_stk_smtp_server)
        self.portEdit.setText(str(config.fb2c_stk_smtp_port))
        self.passwordEdit.setText(config.fb2c_stk_smtp_password)
        self.fromEmailEdit.setText(config.fb2c_stk_from_email)
        self.toEmailEdit.setText(config.fb2c_stk_to_email)

        self.logLevelCombo.setCurrentIndex(self.logLevelCombo.findData(config.fb2c_log_level))
        self.logModeCombo.setCurrentIndex(self.logModeCombo.findData(config.fb2c_log_mode))

        self.onLibroModeSelect()
        self.onCollectFilesCheck()
        self.onConvertConfigModeSelect()

    def onLibroModeSelect(self):
        self.libraryOptionsGroup.setEnabled(not self.converterModeRadio.isChecked())
        self.onCollectFilesCheck()

    def onLibraryRootSelect(self):
        path = uiUtils.getFolder(self, title='Select library root',
                                 defaultPath=self.libraryRootEdit.text())
        if path:
            self.libraryRootEdit.setText(path)

    def onConvertToFolderSelect(self):
        path = uiUtils.getFolder(self, title='Select destination folder',
                                 defaultPath=self.convertToFolderEdit.text())
        if path:
            self.convertToFolderEdit.setText(path)

    def onConverterPathSelect(self):
        if sys.platform == 'win32':
            fileExt = 'fb2c executable (fb2c.exe)'
        else:
            fileExt = 'fb2c executable (fb2c)'
        if len(self.converterPathEdit.text()) > 0:
            defaultPath = os.path.split(self.converterPathEdit.text())[0]
        else:
            defaultPath = None
        files = uiUtils.getFiles(self, title='Select fb2c executable', fileExt=fileExt, defaultPath=defaultPath)
        if files:
            self.converterPathEdit.setText(files[0])

    def onCSSFileSelect(self):
        fileExt = 'Stylesheet (*.css)'
        if len(self.stylesheetFileEdit.text()) > 0:
            defaultPath = os.path.split(self.stylesheetFileEdit.text())[0]
        else:
            defaultPath = None
        files = uiUtils.getFiles(self, title='Select stylesheet', fileExt=fileExt, defaultPath=defaultPath)
        if files:
            self.stylesheetFileEdit.setText(files[0])

    def onConfigFileSelect(self):
        fileExt = 'fb2c configuration (*.toml *.yaml *.json)'
        if len(self.configFileEdit.text()) > 0:
            defaultPath = os.path.split(self.configFileEdit.text())[0]
        else:
            defaultPath = None
        files = uiUtils.getFiles(self, title='Select fb2c configuration file', fileExt=fileExt, defaultPath=defaultPath)
        if files:
            self.configFileEdit.setText(files[0])

    def onCollectFilesCheck(self):
        self.libraryRootEdit.setEnabled(self.collectFilesCheck.isChecked())
        self.libraryRootSelectButton.setEnabled(self.collectFilesCheck.isChecked())
        self.filenamePatternEdit.setEnabled(self.collectFilesCheck.isChecked())

    def onConvertConfigModeSelect(self):
        self.customConfigGroup.setEnabled(self.useCustomConfigRadio.isChecked())
        self.configGroup.setEnabled(not self.useCustomConfigRadio.isChecked())
        self.tabWidget.setTabEnabled(2, not self.useCustomConfigRadio.isChecked())
        self.tabWidget.setTabEnabled(3, not self.useCustomConfigRadio.isChecked())

    def accept(self):
        if config.libro_is_library_mode != self.libraryModeRadio.isChecked():
            config.is_need_restart = True

        config.libro_is_library_mode = self.libraryModeRadio.isChecked()
        config.libro_collect_files = self.collectFilesCheck.isChecked()
        config.libro_library_root_path = self.libraryRootEdit.text()
        config.libro_filename_pattern = self.filenamePatternEdit.currentText()

        config.fb2c_is_custom_config = self.useCustomConfigRadio.isChecked()
        config.fb2c_output_format = self.outputFormatCombo.currentData()
        config.fb2c_convert_to_folder = self.convertToFolderEdit.text()
        config.fb2c_executable_path = self.converterPathEdit.text()
        config.fb2c_custom_config = self.configFileEdit.text()
        config.fb2c_css_file = self.stylesheetFileEdit.text()
        config.fb2c_insert_soft_hyphen = self.insertHyphenCheck.isChecked()
        config.fb2c_notes_mode = self.notesModeCombo.currentData()
        config.fb2c_apnx_mode = self.apnxStyleCombo.currentData()
        config.fb2c_title_format = self.titleFormatEdit.currentText()
        config.fb2c_author_format = self.authorFormatEdit.currentText()

        config.fb2c_stk_smtp_server = self.serverEdit.text()
        try:
            config.fb2c_stk_smtp_port = int(self.portEdit.text())
        except (TypeError, ValueError):
            config.fb2c_stk_smtp_port = 0
        config.fb2c_stk_smtp_password = self.passwordEdit.text()
        config.fb2c_stk_from_email = self.fromEmailEdit.text()
        config.fb2c_stk_to_email = self.toEmailEdit.text()

        config.fb2c_log_level = self.logLevelCombo.currentData()
        config.fb2c_log_mode = self.logModeCombo.currentData()

        super(PreferencesDialog, self).accept()
