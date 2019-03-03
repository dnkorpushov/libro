import os
import json
import codecs


db = None
config_dir = os.path.join(os.path.expanduser('~'), '.libro')
config_file = os.path.join(config_dir, 'config.json')
converter_log_file = os.path.join(config_dir, 'fb2c.log')
default_converter_config = os.path.join(config_dir, 'fb2c_default.toml')
is_need_restart = False

libro_is_library_mode = False
libro_collect_files = False
libro_library_root_path = None
libro_filename_pattern = None

fb2c_executable_path = None
fb2c_output_format = 'mobi'
fb2c_convert_to_folder = None
fb2c_is_custom_config = False
fb2c_custom_config = None
fb2c_css_file = ''
fb2c_insert_soft_hyphen = False
fb2c_notes_mode = 'float'
fb2c_apnx_mode = 'none'
fb2c_title_format = '#title'
fb2c_author_format = '{#f }#l'

fb2c_stk_smtp_server = ''
fb2c_stk_smtp_port = 0
fb2c_stk_smtp_user = ''
fb2c_stk_smtp_password = ''
fb2c_stk_from_email = ''
fb2c_stk_to_email = ''

fb2c_log_level = 'normal'
fb2c_log_mode = 'append'

last_used_open_path = None
last_used_convert_path = None
ui_display_sort_author = False
ui_columns_width = []
ui_splitter_sizes = []
ui_window_x = 0
ui_window_y = 0
ui_window_width = 0
ui_window_height = 0


def load():
    global libro_is_library_mode
    global libro_collect_files
    global libro_library_root_path
    global libro_filename_pattern

    global fb2c_executable_path
    global fb2c_output_format
    global fb2c_convert_to_folder
    global fb2c_is_custom_config
    global fb2c_custom_config
    global fb2c_css_file
    global fb2c_insert_soft_hyphen
    global fb2c_notes_mode
    global fb2c_apnx_mode
    global fb2c_title_format
    global fb2c_author_format

    global fb2c_stk_smtp_server
    global fb2c_stk_smtp_port
    global fb2c_stk_smtp_user
    global fb2c_stk_smtp_password
    global fb2c_stk_from_email
    global fb2c_stk_to_email

    global fb2c_log_level
    global fb2c_log_mode

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
            libro_is_library_mode = c.get('libro_is_library_mode', False)
            libro_collect_files = c.get('libro_collect_files', False)
            libro_library_root_path = c.get('libro_library_root_path', None)
            libro_filename_pattern = c.get('libro_filename_pattern', None)

            fb2c_executable_path = c.get('fb2c_executable_path', None)
            fb2c_output_format = c.get('fb2c_output_format', 'mobi')
            fb2c_convert_to_folder = c.get('fb2c_convert_to_folder', None)
            fb2c_is_custom_config = c.get('fb2c_is_custom_config', False)
            fb2c_custom_config = c.get('fb2c_custom_config', None)
            fb2c_css_file = c.get('fb2c_css_file', '')
            fb2c_insert_soft_hyphen = c.get('fb2c_insert_soft_hyphen', False)
            fb2c_notes_mode = c.get('fb2c_notes_mode', 'float')
            fb2c_apnx_mode = c.get('fb2c_apnx_mode', 'none')
            fb2c_title_format = c.get('fb2c_title_format', '#title')
            fb2c_author_format = c.get('fb2c_author_format', '#f #l')

            fb2c_stk_smtp_server = c.get('fb2c_stk_smtp_server', '')
            fb2c_stk_smtp_port = c.get('fb2c_stk_smtp_port', 0)
            fb2c_stk_smtp_user = c.get('fb2c_stk_smtp_user', '')
            fb2c_stk_smtp_password = c.get('fb2c_stk_smtp_password', '')
            fb2c_stk_from_email = c.get('fb2c_stk_from_email', '')
            fb2c_stk_to_email = c.get('fb2c_stk_to_email', '')

            fb2c_log_level = c.get('fb2c_log_level', 'normal')
            fb2c_log_mode = c.get('fb2c_log_mode', 'append')

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
        'libro_is_library_mode': libro_is_library_mode,
        'libro_collect_files': libro_collect_files,
        'libro_library_root_path': libro_library_root_path,
        'libro_filename_pattern': libro_filename_pattern,

        'fb2c_executable_path': fb2c_executable_path,
        'fb2c_output_format': fb2c_output_format,
        'fb2c_convert_to_folder': fb2c_convert_to_folder,
        'fb2c_is_custom_config': fb2c_is_custom_config,
        'fb2c_custom_config': fb2c_custom_config,
        'fb2c_css_file': fb2c_css_file,
        'fb2c_insert_soft_hyphen': fb2c_insert_soft_hyphen,
        'fb2c_notes_mode': fb2c_notes_mode,
        'fb2c_apnx_mode': fb2c_apnx_mode,
        'fb2c_title_format': fb2c_title_format,
        'fb2c_author_format': fb2c_author_format,

        'fb2c_stk_smtp_server': fb2c_stk_smtp_server,
        'fb2c_stk_smtp_port': fb2c_stk_smtp_port,
        'fb2c_stk_smtp_user': fb2c_stk_smtp_user,
        'fb2c_stk_smtp_password': fb2c_stk_smtp_password,
        'fb2c_stk_from_email': fb2c_stk_from_email,
        'fb2c_stk_to_email': fb2c_stk_to_email,

        'fb2c_log_level': fb2c_log_level,
        'fb2c_log_mode': fb2c_log_mode,

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
