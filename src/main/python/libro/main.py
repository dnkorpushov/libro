from PyQt5.QtCore import QLocale, QTranslator
from fbs_runtime.application_context import ApplicationContext
import sys
from libro.ui.mainwindow import MainWindow


class AppContext(ApplicationContext):
    def run(self):
        locale = QLocale.system().name()[:2]
        qt_locale = ''
        app_locale = ''
        try:
            qt_locale = self.get_resource('locale/qtbase_' + locale + '.qm')
            app_locale = self.get_resource('locale/libro_' + locale + '.qm')
        except FileNotFoundError:
            pass
        if app_locale:
            app_translator = QTranslator()
            app_translator.load(app_locale)
            self.app.installTranslator(app_translator)
        if qt_locale:
            qt_translator = QTranslator()
            qt_translator.load(qt_locale)
            self.app.installTranslator(qt_translator)

        resources = {}
        resources['default_config'] = self.get_resource('fb2cdefault.toml')
        resources['default_css'] = self.get_resource('default.css')

        window = MainWindow(resources)
        window.show()
        return self.app.exec_()


if __name__ == '__main__':
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
