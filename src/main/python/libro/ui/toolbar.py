from PyQt5.QtWidgets import QToolBar, QWidget, QSizePolicy


class ToolBar(QToolBar):
    def __init__(self, parent=None):
        super(ToolBar, self).__init__(parent)

    def addSpacer(self, width=5):
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        spacer.setFixedWidth(width)
        self.addWidget(spacer)

    def addExpandedSpacer(self):
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.addWidget(spacer)

