from enum import Enum

from PyQt5.QtWidgets import qApp, QStyleFactory, QApplication
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt


class AccentColor(Enum):
    default = 0
    blue = 1
    red = 2
    orange = 3
    yellow = 4
    green = 5
    purple = 6
    rose = 7
    gray = 8

    def get_color(value):
        if value == AccentColor.blue:
            return QColor(22, 122, 255)
        elif value == AccentColor.red:
            return QColor(224, 56, 62)
        elif value == AccentColor.orange:
            return QColor(247, 130, 27)
        elif value == AccentColor.yellow:
            return QColor(251, 184, 39)
        elif value == AccentColor.green:
            return QColor(98, 186, 70)
        elif value == AccentColor.purple:
            return QColor(149, 61, 150)
        elif value == AccentColor.rose:
            return QColor(247, 79, 158)
        elif value == AccentColor.gray:
            return QColor(152, 152, 152)
        else:
            return None


class Style(Enum):
    default = 0
    bright = 1
    dark = 2


def setStyle(style, accentColor=0):
    accColor = AccentColor(accentColor)
    if style == Style.default:
        return
    app = QApplication.instance()
    app.setStyle(QStyleFactory.create("Fusion"))
    palette = QPalette()
    if style == Style.dark:
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, QColor(212, 212, 212))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(212, 212, 212))
        app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

    if accColor != accColor.default:
        palette.setColor(QPalette.Highlight, AccentColor.get_color(accColor))

    app.setPalette(palette)
