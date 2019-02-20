import os
import json
import codecs

db = None

converter_config = None
convert_to_folder = None

libro_is_library_mode = False
libro_collect_files = False
libro_library_root_path = None
libro_filename_pattern = None

fb2c_executable_path = None
fb2c_output_format = 'mobi'
fb2c_is_custom_config = False
fb2c_custom_config = None
fb2c_css_file = None
fb2c_insert_soft_hyphen = False
fb2c_notes_mode = 'float'
fb2c_ipnx_mode = 'none'
fb2c_title_format = None
fb2c_author_format = None

fb2c_stk_smtp_server = None
fb2c_stk_smtp_port = None
fb2c_stk_smtp_password = None
fb2c_stk_from_email = None
fb2c_stk_to_email = None

fb2c_log_level = 'normal'
fb2c_log_mode = 'overwrite'

last_used_open_path = None
last_used_convert_path = None
ui_display_sort_author = False
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
    
    global libro_is_library_mode
    global fb2c_is_custom_config

    global last_used_open_path
    global last_used_convert_path
    global ui_display_sort_author
    global ui_columns_width
    global ui_splitter_sizes
    global ui_window_x
    global ui_window_y
    global ui_window_width
    global ui_window_height

    if os.path.exists(config_file):
        with codecs.open(config_file, 'r', encoding='utf-8') as f:
            c = json.loads(f.read())
            converter_path = c.get('converter_path', None)
            converter_config = c.get('converter_config', None)
            convert_to_folder = c.get('convert_to_folder', None)
            output_format = c.get('output_format', 'epub')

            libro_is_library_mode = c.get('libro_is_library_mode', False)
            fb2c_is_custom_config = c.get('fb2c_is_custom_config', False)

            last_used_open_path = c.get('last_used_open_path', None)
            last_used_convert_path = c.get('last_used_convert_path', None)
            ui_display_sort_author = c.get('ui_display_sort_author', False)
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

        'libro_is_library_mode': libro_is_library_mode,
        'fb2c_is_custom_config': fb2c_is_custom_config,

        'last_used_open_path': os.path.normpath(last_used_open_path) if last_used_open_path else None,
        'last_used_convert_path': os.path.normpath(last_used_convert_path) if last_used_convert_path else None,

        'ui_display_sort_author': ui_display_sort_author,
        'ui_columns_width': ui_columns_width,
        'ui_splitter_sizes': ui_splitter_sizes,
        'ui_window_x': ui_window_x,
        'ui_window_y': ui_window_y,
        'ui_window_width': ui_window_width,
        'ui_window_height': ui_window_height
    }
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    with codecs.open(config_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(c, sort_keys=False, indent=4))
