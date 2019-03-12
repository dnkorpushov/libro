import os
import zipfile
from lxml import etree

from libro.utils.bookmeta import BookMeta


class EpubMeta:
    file = ''
    version = ''
    tree = None
    content_root = ''
    opf_file = ''

    zip = None

    ns = {
        'n': 'urn:oasis:names:tc:opendocument:xmlns:container',
        'opf': 'http://www.idpf.org/2007/opf',
        'dc': 'http://purl.org/dc/elements/1.1/'
    }

    def __init__(self, file):
        self.file = file
        self.zip = zipfile.ZipFile(self.file)
        container = self.zip.read('META-INF/container.xml')
        tree = etree.fromstring(container)
        self.opf_file = tree.xpath('n:rootfiles/n:rootfile/@full-path', namespaces=self.ns)[0]
        opf = self.zip.read(self.opf_file)
        self.content_root = os.path.split(self.opf_file)[0]
        if self.content_root:
            self.content_root += '/'
        self.tree = etree.fromstring(opf)
        v = self.tree.xpath('/opf:package/@version', namespaces=self.ns)[0]
        self.version = v[:1]

    def get_metadata(self):
        metadata = BookMeta()
        metadata.title = self._get_value('title')
        metadata.author = self._get_authors()
        metadata.series = self._get_series()
        metadata.series_index = self._get_series_index()
        metadata.tag = self._get_subject()
        metadata.description = self._get_value('description')
        metadata.translator = ''
        metadata.lang = self._get_value('language')
        metadata.date = self._get_value('date')
        metadata.publisher = self._get_value('publisher')
        metadata.cover_image_name, metadata.cover_image_data = self._get_cover()
        metadata.format = 'epub'

        return metadata

    def set_metadata(self, metadata):
        pass

    def _get_series(self):
        series = self._find('meta[@name="calibre:series"]', namespace='opf')
        if series is not None and 'content' in series.attrib:
            return series.attrib['content']
        else:
            return ''

    def _get_series_index(self):
        series_index = self._find('meta[@name="calibre:series_index"]', namespace='opf')
        if series_index is not None and 'content' in series_index.attrib:
            return series_index.attrib['content']
        else:
            return ''

    def _get_subject(self):
        subject_list = []
        node_list = self._findall('subject')
        for n in node_list:
            subject_list.append(n.text)
        return subject_list

    def _get_authors(self):
        author_list = []
        if self.version == '2':
            node_list = self._findall('creator[@opf:role="aut"]')
            for n in node_list:
                author_list.append(n.text)

        elif self.version == '3':
            node_list = self._findall('creator')
            for n in node_list:
                try:
                    author_id = n.attrib['id']
                    role = self._find('meta[@refines="#{}" and @property="role"]/text()'.format(author_id),
                                      namespace='opf')
                    if role is None or role == 'aut':
                        author_list.append(n.text)
                except KeyError:
                    pass

        if len(author_list) == 0:
            node_list = self._findall('creator')
            for n in node_list:
                author_list.append(n.text)

        return author_list

    def _get_cover(self):
        cover_name = ''
        cover_data = None
        node = self._find('meta[@name="cover"]', namespace='opf')
        if node is not None:
            try:
                cover_id = node.attrib['content']
                node_list = self.tree.xpath('/opf:package/opf:manifest/opf:item[@id="{}"]'.format(cover_id),
                                            namespaces=self.ns)
                for n in node_list:
                    try:
                        cover_name = n.attrib['href']
                        break
                    except KeyError:
                        pass
            except KeyError:
                pass
        else:
            node_list = self.tree.xpath('/opf:package/opf:manifest/opf:item[@properties="cover-image"]',
                                        namespaces=self.ns)
            for n in node_list:
                try:
                    cover_name = n.attrib['href']
                    break
                except KeyError:
                    pass
        if cover_name:
            cover_data = self.zip.read(self.content_root + cover_name)

        return cover_name, cover_data

    def _get_value(self, name):
        value = self._find(name)
        return value.text if value is not None else ''

    def _set_value(self, name, text):
        value = self._find(name)
        if value is None:
            pass
        value.text = text

    def _find(self, name, namespace='dc'):
        node_list = self.tree.xpath('/opf:package/opf:metadata/{}:{}'.format(namespace, name), namespaces=self.ns)
        for n in node_list:
            return n

    def _findall(self, name, namespace='dc'):
        return self.tree.xpath('/opf:package/opf:metadata/{}:{}'.format(namespace, name), namespaces=self.ns)
