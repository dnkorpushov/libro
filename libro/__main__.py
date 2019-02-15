import sys
from PyQt5.QtWidgets import QApplication

from libro.ui.mainwindow import MainWindow


class Application(QApplication):
    def __init__(self, argv):        
        super(Application, self).__init__(argv)


if __name__ == '__main__':
    app = Application(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
