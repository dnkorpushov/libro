from fbs.cmdline import command
from glob import glob
from subprocess import call

import os
import fbs.cmdline

UI_SRCPATH = 'src/main/designer'
UI_DESTPATH = 'src/main/python/libro/ui'


@command
def ui():
    for ui_file in glob(os.path.join(UI_SRCPATH, '*.ui')):
        py_file = os.path.join(UI_DESTPATH, os.path.splitext(os.path.split(ui_file)[1])[0] + '_ui.py')
        ui_file = os.path.normpath(ui_file)
        py_file = os.path.normpath(py_file)
        call('pyuic5 --from-imports {} -o {}'.format(ui_file, py_file), shell=True)


@command
def rc():
    for rc_file in glob(os.path.join(UI_SRCPATH, '*.qrc')):
        py_file = os.path.join(UI_DESTPATH, os.path.splitext(os.path.split(rc_file)[1])[0] + '_rc.py')
        rc_file = os.path.normpath(rc_file)
        py_file = os.path.normpath(py_file)
        call('pyrcc5 {} -o {}'.format(rc_file, py_file), shell=True)


if __name__ == '__main__':
    project_dir = os.path.dirname(__file__)
    fbs.cmdline.main(project_dir)
