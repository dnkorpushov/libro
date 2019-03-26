import os
import json
import codecs

# Runtime config variables
db = None
config_dir = os.path.join(os.path.expanduser('~'), '.libro')
config_file = os.path.join(config_dir, 'config.json')
converter_log_file = os.path.join(config_dir, 'fb2c.log')
default_converter_config = os.path.join(config_dir, 'fb2c_default.toml')
device_path = ''
is_need_restart = False

# Preferences: General
is_library_mode = False
collect_files = False
library_root_path = None
filename_pattern = None
device_path = None

# Preferences: Convert
converter_output_format = 'mobi'
converter_executable_path = None
converter_config = None

# UI saved variables
last_used_open_path = None
last_used_convert_path = None
ui_display_sort_author = False
ui_columns_width = []
ui_splitter_sizes = []
ui_window_x = 0
ui_window_y = 0
ui_window_width = 0
ui_window_height = 0


def check_mail_settings():
    pass
    # if (fb2c_stk_smtp_server and fb2c_stk_smtp_port > 0 and
    #         fb2c_stk_smtp_user and fb2c_stk_smtp_password and fb2c_stk_to_email and
    #         fb2c_stk_from_email and fb2c_output_format == 'mobi'):
    #     return True
    # return False


def load():
    global is_library_mode
    global collect_files
    global library_root_path
    global filename_pattern
    global device_path

    global converter_output_format
    global converter_executable_path
    global converter_config

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
            is_library_mode = c.get('is_library_mode', False)
            collect_files = c.get('collect_files', False)
            library_root_path = c.get('library_root_path', '')
            filename_pattern = c.get('filename_pattern', '')
            device_path = c.get('device_path', '')

            converter_output_format = c.get('converter_output_format', 'mobi')
            converter_executable_path = c.get('converter_executable_path', '')
            converter_config = c.get('converter_config', '')

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
        'is_library_mode': is_library_mode,
        'collect_files': collect_files,
        'library_root_path': library_root_path,
        'filename_pattern': filename_pattern,
        'device_path': device_path,
        'converter_output_format': converter_output_format,
        'converter_executable_path': converter_executable_path,
        'converter_config': converter_config,

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
