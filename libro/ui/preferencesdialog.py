from PyQt5.QtWidgets import QDialog

from libro.ui.preferencesdialog_ui import Ui_Dialog
import libro.config as config


class PreferencesDialog(QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(PreferencesDialog, self).__init__(parent)
        self.setupUi(self)
        self.initValues()

    def initValues(self):
        for item in ['epub', 'mobi', 'azw3', 'kepub']:
            self.outputFormatCombo.addItem(item, item)
        for item in ['default', 'float', 'block', 'inline']:
            self.notesModeCombo.addItem(item, item)
        for item in ['none', 'eink', 'app']:
            self.apnxStyleCombo.addItem(item, item)

        self.libraryModeRadio.setChecked(config.libro_is_library_mode)
        self.converterModeRadio.setChecked(not config.libro_is_library_mode)

        self.useCustomConfigRadio.setChecked(config.fb2c_is_custom_config)
        self.useDefaultConfigRadio.setChecked(not config.fb2c_is_custom_config)

        self.onLibroModeSelect()
        self.onCollectFilesCheck()
        self.onConvertConfigModeSelect()

    def onLibroModeSelect(self):
        self.libraryOptionsGroup.setEnabled(not self.converterModeRadio.isChecked())
        self.onCollectFilesCheck()

    def onLibraryRootSelect(self):
        pass

    def onCollectFilesCheck(self):
        self.libraryRootEdit.setEnabled(self.collectFilesCheck.isChecked())
        self.libraryRootSelectButton.setEnabled(self.collectFilesCheck.isChecked())
        self.filenamePatternEdit.setEnabled(self.collectFilesCheck.isChecked())

    def onConvertConfigModeSelect(self):
        self.customConfigGroup.setEnabled(self.useCustomConfigRadio.isChecked())
        self.configGroup.setEnabled(not self.useCustomConfigRadio.isChecked())
        self.tabWidget.setTabEnabled(2, not self.useCustomConfigRadio.isChecked())
        self.tabWidget.setTabEnabled(3, not self.useCustomConfigRadio.isChecked())
