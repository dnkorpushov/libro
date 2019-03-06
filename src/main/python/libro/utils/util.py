import os
import sys
import psutil


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
                return fs
            elif (os.path.exists(os.path.join(fs, 'system', 'thumbnails'))
                    and os.path.exists(os.path.join(fs, 'system', 'version.txt'))):
                # Kindle Paperwhite, Voyage, Oasis
                return fs
    return ''
