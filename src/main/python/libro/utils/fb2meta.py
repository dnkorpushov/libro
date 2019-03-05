from lxml import etree
from lxml.etree import QName

import base64
from io import BytesIO

from libro.utils.bookmeta import BookMeta, Author
from libro.utils.myzipfile import ZipFile


class Fb2Meta:
    def __init__(self, file):
        self.ns = {'fb': 'http://www.gribuser.ru/xml/fictionbook/2.0'}
        self.file = file
        self.tree = None
        self.encoding = None
        self.zip_info = None

        if file.lower().endswith('.zip'):
            with ZipFile(self.file, mode='r') as z:
                self.zip_info = z.infolist()[0]
                with z.open(self.zip_info, mode='r') as f:
                    self.tree = etree.parse(BytesIO(f.read()), parser=etree.XMLParser(recover=True))
                z.close()
        else:
            self.tree = etree.parse(file, parser=etree.XMLParser(recover=True))
        self.encoding = self.tree.docinfo.encoding

    def get_meta(self):
        meta = BookMeta()
        meta.title = self._get_title()
        meta.author = self._get_author_list()
        meta.series, meta.series_index = self._get_series()
        meta.tag = self._get_tags()
        meta.translator = self._get_translator_list()
        meta.lang = self._get_lang()
        meta.src_lang = self._get_lang(src_lang=True)
        meta.date = self._get_date()
        meta.description = self._get_description()
        meta.cover_image_name, meta.cover_image_data = self._get_cover()
        return meta

    def set_meta(self, meta):
        # Generate new title-info for fb2
        nsmap = {None: 'http://www.gribuser.ru/xml/fictionbook/2.0', 'l': 'http://www.w3.org/1999/xlink'}
        title_info = etree.Element('title-info', nsmap=nsmap)
        etree.SubElement(title_info, 'book-title').text = meta.title
        for author in meta.author:
            node = self._create_person_node('author', author)
            title_info.append(node)
        for tag in meta.tag:
            etree.SubElement(title_info, 'genre').text = tag
        if meta.series:
            series_node = etree.SubElement(title_info, 'sequence')
            series_node.attrib['name'] = meta.series
            if meta.series_index:
                series_node.attrib['number'] = str(meta.series_index)
        if meta.description:
            node = etree.SubElement(title_info, 'annotation')
            etree.SubElement(node, 'p').text = meta.description
        if meta.date:
            etree.SubElement(title_info, 'date').text = meta.date
        if meta.cover_image_name:
            node = etree.SubElement(title_info, 'coverpage')
            image_node = etree.SubElement(node, 'image')
            image_node.attrib[QName('http://www.w3.org/1999/xlink', 'href')] = '#{}'.format(meta.cover_image_name)
        if meta.lang:
            etree.SubElement(title_info, 'lang').text = meta.lang
        if meta.src_lang:
            etree.SubElement(title_info, 'src-lang').text = meta.src_lang
        for translator in meta.translator:
            node = self._create_person_node('translator', translator)
            title_info.append(node)

        # replace original title-info
        title_node = self._find('//fb:description/fb:title-info')
        title_node.getparent().replace(title_node, title_info)

        # Change cover image
        if meta.cover_image_name and meta.cover_image_data is not None:
            node = self._find('//fb:binary[@id="{0}"]'.format(meta.cover_image_name))
            if node is None:
                node = etree.SubElement(self.tree.getroot(), 'binary')
            node.attrib['id'] = meta.cover_image_name
            node.attrib['content-type'] = 'image/jpeg'
            node.text = base64.encodebytes(meta.cover_image_data)

    def save(self):
        if self.file.lower().endswith('.zip'):
            with ZipFile(self.file, mode='w') as z:
                    z.writestr(self.zip_info, etree.tostring(self.tree, encoding=self.encoding,
                                                             method='xml', xml_declaration=True, pretty_print=True))
        else:
            self.tree.write(self.file, encoding=self.encoding, method='xml', xml_declaration=True, pretty_print=True)

    def _create_person_node(self, node_name, person):
        node = etree.Element(node_name)
        if person.first_name:
            etree.SubElement(node, 'first-name').text = person.first_name
        if person.middle_name:
            etree.SubElement(node, 'middle-name').text = person.middle_name
        if person.last_name:
            etree.SubElement(node, 'last-name').text = person.last_name

        return node

    def _get_date(self):
        date = self._find('//fb:description/fb:title-info/fb:date')
        if date is not None:
            return date.text
        return ''

    def _get_cover(self):
        cover_name = ''
        cover_data = None
        cover = self._find('//fb:description/fb:title-info/fb:coverpage/fb:image')
        if cover is not None:
            for a in cover.attrib:
                if QName(a).localname == 'href':
                    cover_name = cover.attrib[a][1:]
                    node = self._find('//fb:binary[@id="{0}"]'.format(cover_name))
                    if node is not None:
                        cover_data = base64.b64decode(node.text.encode('ascii'))

                    return cover_name, cover_data

    def _get_description(self):
        annotation = self._find('//fb:description/fb:title-info/fb:annotation')
        if annotation is not None:
            return ''.join(annotation.itertext())
        return ''

    def _get_lang(self, src_lang=False):
        if src_lang:
            lang = self._find('//fb:description/fb:title-info/fb:src-lang')
        else:
            lang = self._find('//fb:description/fb:title-info/fb:lang')
        return lang.text if lang is not None else ''

    def _get_title(self):
        title = self._find('//fb:description/fb:title-info/fb:book-title')
        return title.text if title is not None else ''

    def _get_translator_list(self):
        node_list = self._findall('//fb:description/fb:title-info/fb:translator')
        translator_list = []
        for node in node_list:
            translator = self._get_author(node)
            translator_list.append(translator)
        return translator_list

    def _get_author_list(self):
        node_list = self._findall('//fb:description/fb:title-info/fb:author')
        author_list = []
        for node in node_list:
            author = self._get_author(node)
            author_list.append(author)
        return author_list

    def _get_author(self, node):
        author = Author()
        for e in node:
            if QName(e).localname == 'first-name':
                author.first_name = e.text
            elif QName(e).localname == 'middle-name':
                author.middle_name = e.text
            elif QName(e).localname == 'last-name':
                author.last_name = e.text
        return author

    def _get_tags(self):
        tags = []
        node_list = self._findall('//fb:description/fb:title-info/fb:genre')
        for n in node_list:
            tags.append(n.text)
        return tags

    def _get_series(self):
        series_name = ''
        series_index = ''
        series = self._find('//fb:description/fb:title-info/fb:sequence')
        if series is not None:
            series_name = series.attrib['name'] if 'name' in series.attrib else ''
            series_index = series.attrib['number'] if 'number' in series.attrib else ''

        return (series_name, series_index)

    def _find(self, xpath):
        node_list = self.tree.xpath(xpath, namespaces=self.ns)
        for n in node_list:
            return n

    def _findall(self, xpath):
        return self.tree.xpath(xpath, namespaces=self.ns)
