import os
import sys
import psutil
import codecs
import tomlkit
import json
import ebookmeta

from lxml import etree


def is_supported_format(file):
    if file.lower().endswith(('.fb2', '.fb2.zip', '.zip', '.epub')):
        return True
    else:
        return False


def format_pattern(s, seq):

    def replace_keyword(pict, k, v):
        if pict.count(k) > 0:
            return pict.replace(k, v), True if v else False
        return pict, False

    def replace_keywords(pict, seq):
        expanded = False
        for (k, v) in seq:
            pict, ok = replace_keyword(pict, k, v)
            expanded = expanded or ok
        if not expanded:
            return ''
        return pict

    p_o = -1
    p_c = -1

    # Hack - I do not want to write real parser
    pps = s.replace(r'\{', chr(1)).replace(r'\}', chr(2))

    for i, sym in enumerate(pps):
        if sym == '{':
            p_o = i
        elif sym == '}':
            p_c = i
            break

    if p_o >= 0 and p_c > 0 and p_o < p_c:
        pps = format_pattern(pps[0:p_o] + replace_keywords(pps[p_o + 1:p_c], seq) + pps[p_c + 1:], seq)
    else:
        pps = replace_keywords(pps, seq)

    return pps.replace(chr(1), '{').replace(chr(2), '}')


# Find kindle device mountpoint
def find_reader_device():
    mounted_fs = []

    if sys.platform == 'darwin':
        list_dir = os.listdir('/Volumes')
        for dir_name in list_dir:
            mounted_fs.append(os.path.join('/Volumes', dir_name))
    else:
        mounted_list = psutil.disk_partitions()
        for fs in mounted_list:
            if fs.fstype:
                mounted_fs.append(fs.mountpoint)
    for fs in mounted_fs:
        dir_documents = os.path.join(fs, 'documents')
        dir_system = os.path.join(fs, 'system')

        if os.path.exists(dir_documents) and os.path.exists(dir_system):
            if os.path.exists(os.path.join(fs, 'system', 'com.amazon.ebook.booklet.reader', 'reader.pref')):
                # Kindle 4, 5
                return os.path.join(fs, 'documents')
            elif (os.path.exists(os.path.join(fs, 'system', 'thumbnails'))
                    and os.path.exists(os.path.join(fs, 'system', 'version.txt'))):
                # Kindle Paperwhite, Voyage, Oasis
                return os.path.join(fs, 'documents')
    return ''


def set_converter_log_file(converter_config, log_file):
    if os.path.exists(converter_config):
        with codecs.open(converter_config, mode='r', encoding='utf-8') as f:
            doc = tomlkit.loads(f.read())
            f.close()

        doc['logger']['file']['level'] = 'normal'
        doc['logger']['file']['destination'] = log_file
        doc['logger']['file']['mode'] = 'overwrite'

        with codecs.open(converter_config, mode='w', encoding='utf-8') as f:
            f.write(tomlkit.dumps(doc))
            f.close()


def check_mail_setings(converter_config):
    host = ''
    port = ''
    user = ''
    password = ''

    if os.path.exists(converter_config):
        with codecs.open(converter_config, mode='r', encoding='utf-8') as f:
            doc = tomlkit.loads(f.read())
            f.close()

            try:
                host = doc['sendtokindle']['smtp_server']
                port = doc['sendtokindle']['smtp_port']
                user = doc['sendtokindle']['smtp_user']
                password = doc['sendtokindle']['smtp_password']
            except KeyError:
                pass

    if host and port and user and password:
        return True
    else:
        return False


def get_convert_result(log_file):
    data = []
    src = ''
    dst = ''
    err = []
    err_text = ''
    if os.path.exists(log_file):
        with codecs.open(log_file, mode='r', encoding='utf-8') as f:
            data = f.readlines()
            f.close()
        for line in data:
            elem = line.split('\t')
            info = json.loads(elem[4])
            try:
                src = info['source']
            except KeyError:
                pass
            try:
                dst = info['to']
            except KeyError:
                pass

            if elem[1] in ('ERROR', 'WARN'):
                try:
                    err_text = info['error']
                except KeyError:
                    err_text = ''
                err.append((elem[1], '{}: {}'.format(elem[3], err_text)))
        return src, dst, err


def insert_substring(string, substring):
    if string:
        words = string.split(',')
        for word in words:
            if word.strip() == substring:
                return string

        if string[-1] == ' ':
            string = string[0:-1]
        if string[-1] == ',':
            string = string[0:-1]
        return '{0}, {1}'.format(string.strip(), substring)
    else:
        return substring


def get_genres_menu_data(lang='ru'):
    if lang not in ['ru', 'en']:
        lang = 'en'
    genres = etree.fromstring(ebookmeta.fb2genres.fb2genres, parser=etree.XMLParser())

    genre_menu = []

    for genre in genres:
        genre_value = genre.attrib['value']
        genre_name = ''
        for genre_data in genre:
            subgenre_menu = []
            if genre_data.tag == 'root-descr' and genre_data.attrib['lang'] == lang:
                genre_name = genre_data.attrib['genre-title']
            elif genre_data.tag == 'subgenres':
                for subgenre in genre_data:
                    subgenre_value = subgenre.attrib['value']
                    subgenre_name = ''
                    for subgenre_data in subgenre:
                        if subgenre_data.tag == 'genre-descr' and subgenre_data.attrib['lang'] == lang:
                            subgenre_name = subgenre_data.attrib['title']
                    subgenre_menu.append({'value': subgenre_value, 'title': subgenre_name})

        genre_menu.append({'value': genre_value, 'title': genre_name, 'submenu': subgenre_menu})
    return genre_menu
