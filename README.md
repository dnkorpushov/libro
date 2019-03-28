# Libro

Ebook library manager for files in fb2 (fb2.zip) and epub (v2, v3) formats and GUI for [fb2converter](https://github.com/rupor-github/fb2converter) for Windows, macOS and Linux.

[Manual (Russian)](https://github.com/dnkorpushov/libro/wiki)

## Setup
Install Python 3.7.

Install PyQt5, [fbs](https://github.com/mherrmann/fbs), pyInstaller:
```
python3 -m pip install fbs, PyQt5, pyInstaller
```

Clone project:
```
git clone https://github.com/dnkorpushov/libro.git
```

Install required libraries:
```
cd libro
python3 -m pip install -r requirements/base.txt
```

## Run
To run application execute following command:
```
python3 build.py run
```

## Build
I use [fman build system](https://github.com/mherrmann/fbs) with some custom extensions to build application.
See below for the most useable commands.

Translate qt designer forms to python code:
```
python3 build.py ui
```

Translate qt designer forms to python code:
```
python3 build.py rc
```

Build locale source files for translate/compile locale source file to binary qm files:
```
python3 build.py locale
```

Build standalone executable:
```
python3 build.py freeze
```

Build installer (for Microsoft Windows install [NSIS](http://nsis.sourceforge.net/Main_Page) before execute following command):
```
python3 build.py installer
```

See [fbs manual](https://build-system.fman.io/manual/) for more information.





