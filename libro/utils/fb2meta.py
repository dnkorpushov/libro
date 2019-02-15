#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import os

from zipfile import ZipFile, ZipInfo

from io import BytesIO
from lxml import etree
from lxml.etree import QName

def get_metadata(file, read_cover_image=False):
    metadata = {}

    meta = Fb2Meta(file)
    meta.get_metadata(read_cover_image)

    series, series_num = meta.get_first_series()

    metadata['title'] = meta.book_title
    metadata['authors'] = meta.get_autors()
    metadata['description'] = meta.annotation
    metadata['tags'] = meta.genre
    metadata['lang'] = meta.lang
    metadata['series'] = series
    metadata['series_num'] = series_num
    if read_cover_image:
        metadata['coverimage'] = meta.coverdata
        if meta.coverpage:
            metadata['coverimage_type'] = os.path.splitext(meta.coverpage)[1].lower()[1:]

    return metadata


class Author():
    def __init__(self):
        self.first_name = ''
        self.middle_name = ''
        self.last_name = ''


class Sequence():
    def __init__(self):
        self.name = ''
        self.number = None


class Fb2Meta():
    def __init__(self, file):
        self.file = file

        self.genre = []
        self.author = []
        self.book_title = ''
        self.annotation = None
        self.keywords = None
        self.date = None
        self.coverpage = ''
        self.lang = 'ru'
        self.src_lang = ''
        self.translator = []
        self.sequence = []

        self.coverdata = None
        self.coverpage_href = ''
        self.is_zip = False
        self.encoding = ''
        self.zip_info = ZipInfo()

        if os.path.splitext(self.file)[1].lower() == '.zip':
            self.is_zip = True

        if self.is_zip:
            with ZipFile(self.file) as myzip:
                # TODO - warn here if len(myzip.infolist) > 1?
                self.zip_info = myzip.infolist()[0]
                with myzip.open(self.zip_info, 'r') as myfile:
                    self.tree = etree.parse(BytesIO(myfile.read()), parser=etree.XMLParser(recover=True))
                    self.encoding = self.tree.docinfo.encoding
        else:
            self.tree = etree.parse(self.file, parser=etree.XMLParser(recover=True))
            self.encoding = self.tree.docinfo.encoding

    def get_first_series(self):
        series_name = ''
        series_num = ''
        for series in self.sequence:
            series_name = series.name
            series_num = series.number

        return (series_name, series_num)

    def get_autors(self):
        author_str = ''

        for author in self.author:
            if len(author_str) > 0:
                author_str += ', '

            if author.first_name:
                author_str += author.first_name
            if author.middle_name:
                author_str += ' ' + author.middle_name
            if author.last_name:
                author_str += ' ' + author.last_name

        return author_str.replace('  ', ' ').strip()

    def get_metadata(self, read_cover_image=False):
        ns = {'fb': 'http://www.gribuser.ru/xml/fictionbook/2.0'}
        for title_info in self.tree.xpath('//fb:description/fb:title-info', namespaces=ns):
            for elem in title_info:
                if QName(elem).localname == 'genre':
                    self.genre.append(elem.text)
                elif QName(elem).localname == 'author':
                    author = Author()
                    for e in elem:
                        if QName(e).localname == 'first-name':
                            author.first_name = e.text
                        elif QName(e).localname == 'middle-name':
                            author.middle_name = e.text
                        elif QName(e).localname == 'last-name':
                            author.last_name = e.text
                    self.author.append(author)
                elif QName(elem).localname == 'book-title':
                    self.book_title = elem.text
                elif QName(elem).localname == 'annotation':
                    self.annotation = etree.tostring(elem, method='text', encoding='utf-8').decode('utf-8').strip()
                elif QName(elem).localname == 'keywords':
                    self.keywords = elem
                elif QName(elem).localname == 'date':
                    self.date = elem
                elif QName(elem).localname == 'coverpage':
                    for e in elem:
                        if QName(e).localname == 'image':
                            for attrib in e.attrib:
                                if QName(attrib).localname == 'href':
                                    self.coverpage = e.attrib[attrib][1:]
                                    self.coverpage_href = attrib
                elif QName(elem).localname == 'lang':
                    self.lang = elem.text
                elif QName(elem).localname == 'src-lang':
                    self.src_lang = elem.text
                elif QName(elem).localname == 'translator':
                    self.translator.append(elem)
                elif QName(elem).localname == 'sequence':
                    seq = Sequence()
                    for a in elem.attrib:
                        if a == 'name':
                            seq.name = elem.attrib[a]
                        elif a == 'number':
                            seq.number = elem.attrib[a]
                    self.sequence.append(seq)

        if self.coverpage and read_cover_image:
            for tag in self.tree.xpath('//fb:binary[@id="{0}"]'.format(self.coverpage), namespaces=ns):
                self.coverdata = base64.b64decode(tag.text.encode('ascii'))
