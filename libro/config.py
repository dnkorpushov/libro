import os
import json
import codecs

db = None

converter_path = None
converter_config = None
convert_to_folder = None
output_format = 'mobi'
library_mode = False
last_used_open_path = None
last_used_convert_path = None
ui_columns_width = []
ui_splitter_sizes = []
ui_window_x = 0
ui_window_y = 0
ui_window_width = 0
ui_window_height = 0

config_dir = os.path.join(os.path.expanduser('~'), '.libro')
config_file = os.path.join(config_dir, 'config.json')


def load():
    global converter_path
    global converter_config
    global convert_to_folder
    global output_format
    global library_mode
    global last_used_open_path
    global last_used_convert_path
    global ui_columns_width
    global ui_splitter_sizes
    global ui_window_x
    global ui_window_y
    global ui_window_width
    global ui_window_height

    if os.path.exists(config_file):
        with codecs.open(config_file, 'r') as f:
            c = json.loads(f.read())
            converter_path = c.get('converter_path', None)
            converter_config = c.get('converter_config', None)
            convert_to_folder = c.get('convert_to_folder', None)
            output_format = c.get('output_format', 'epub')
            library_mode = c.get('library_mode', False)
            last_used_open_path = c.get('last_used_open_path', None)
            last_used_convert_path = c.get('last_used_convert_path', None)
            ui_columns_width = c.get('ui_columns_width', [])
            ui_splitter_sizes = c.get('ui_splitter_sizes', [])
            ui_window_x = c.get('ui_window_x', 0)
            ui_window_y = c.get('ui_window_y', 0)
            ui_window_width = c.get('ui_window_width', 0)
            ui_window_height = c.get('ui_window_height', 0)


def save():
    c = {
        'converter_path': os.path.normpath(converter_path) if converter_path else None,
        'converter_config': os.path.normpath(converter_config) if converter_config else None,
        'convert_to_folder': os.path.normpath(convert_to_folder) if convert_to_folder else None,
        'output_format': output_format,
        'library_mode': library_mode,
        'last_used_open_path': os.path.normpath(last_used_open_path) if last_used_open_path else None,
        'last_used_convert_path': os.path.normpath(last_used_convert_path) if last_used_convert_path else None,
        'ui_columns_width': ui_columns_width,
        'ui_splitter_sizes': ui_splitter_sizes,
        'ui_window_x': ui_window_x,
        'ui_window_y': ui_window_y,
        'ui_window_width': ui_window_width,
        'ui_window_height': ui_window_height
    }
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    with codecs.open(config_file, 'w') as f:
        f.write(json.dumps(c, sort_keys=False, indent=4))
