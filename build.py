import sys
import os
import shutil

from subprocess import call
from glob import glob


INSTALLER_SPEC = os.path.join('misc', 'libro.spec')
UI_SRCPATH = 'designer'
UI_DESTPATH = 'libro/ui'


def clean():
    shutil.rmtree('build')
    shutil.rmtree('dist')


def build_ui():
    for ui_file in glob(os.path.join(UI_SRCPATH, '*.ui')):
        py_file = os.path.join(UI_DESTPATH, os.path.splitext(os.path.split(ui_file)[1])[0] + '_ui.py')
        ui_file = os.path.normpath(ui_file)
        py_file = os.path.normpath(py_file)
        call('pyuic5 --from-imports {} -o {}'.format(ui_file, py_file), shell=True)


def build_rc():
    for rc_file in glob(os.path.join(UI_SRCPATH, '*.qrc')):
        py_file = os.path.join(UI_DESTPATH, os.path.splitext(os.path.split(rc_file)[1])[0] + '_rc.py')
        rc_file = os.path.normpath(rc_file)
        py_file = os.path.normpath(py_file)
        call('pyrcc5 {} -o {}'.format(rc_file, py_file), shell=True)


def freeze_app():
    print(INSTALLER_SPEC)
    call('pyinstaller {} --noconfirm --clean'.format(INSTALLER_SPEC), shell=True)


def print_usage():
    print('''
Usage: python build.py <command>
available commands:
    freeze  Build freeze app.
    ui      Build .ui forms.
    rc      Build .qrc resources.
    clean   Clean project.
        ''')


def main():
    if len(sys.argv) == 2:
        cmd = sys.argv[1]
        if cmd == 'ui':
            build_ui()
        elif cmd == 'rc':
            build_rc()
        elif cmd == 'freeze':
            freeze_app()
        elif cmd == 'clean':
            clean()
        else:
            print_usage()
    else:
        print_usage()


if __name__ == '__main__':
    main()
