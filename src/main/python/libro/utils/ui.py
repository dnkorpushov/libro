import os
from PyQt5.QtWidgets import QFileDialog


def getFolder(parent, title, defaultPath=None):
    dlg = QFileDialog(parent, title)
    dlg.setFileMode(QFileDialog.Directory)
    dlg.setOption(QFileDialog.ShowDirsOnly, True)

    if defaultPath:
        dlg.setDirectory(defaultPath)

    if dlg.exec_():
        return os.path.normpath(dlg.selectedFiles()[0])
    else:
        return None


def getFiles(parent, title, fileExt, defaultPath=None, multipleSelect=False):
    dlg = QFileDialog(parent, title)
    if defaultPath:
        dlg.setDirectory(defaultPath)
    if multipleSelect:
        dlg.setFileMode(QFileDialog.ExistingFiles)
    else:
        dlg.setFileMode(QFileDialog.ExistingFile)
    dlg.setNameFilters([fileExt, 'All files (*.*)'])

    if dlg.exec_():
        normFiles = []
        files = dlg.selectedFiles()
        for f in files:
            normFiles.append(os.path.normpath(f))
        return normFiles

    else:
        return None
