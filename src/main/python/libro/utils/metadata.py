import epub_meta
import base64

from libro.utils.fb2meta import Fb2Meta
from .tags import tag_translate


def set_metadata(meta):
    if meta.book_format == 'fb2':
        fb2meta = Fb2Meta(meta.file)
        fb2meta.set_meta(meta)
        fb2meta.save()


def get_metadata(file):
    book_type = None
    if file.lower().endswith(('.fb2', '.fb2.zip', '.zip')):
        book_type = 'fb2'
    elif file.lower().endswith('.epub'):
        book_type = 'epub'
    else:
        book_type = 'unknown'

    if book_type == 'fb2':
        fb2meta = Fb2Meta(file)
        metadata = fb2meta.get_meta()

    metadata.file = file
    metadata.book_format = book_type
    return metadata

#####################################


def translate_tags(tags):
    i = 0
    for t in tags:
        if t in tag_translate.keys():
            tags[i] = tag_translate[t]
        i += 1

    return ', '.join(tags)


def format_author(author):
    words = author.strip().split()
    if len(words) > 1:
        words.insert(0, words.pop())
        return ' '.join(words)
    else:
        return author


class Metadata:
    def __init__(self, file):
        self.file = file
        self.type = None

        self.author = ''
        self.author_sort = ''
        self.title = ''
        self.description = ''
        self.tags = ''
        self.lang = 'ru'
        self.translator = ''
        self.series = ''
        self.series_index = None
        self.coverimage = None
        self.coverimage_type = None

        if file.lower().endswith(('.fb2', '.fb2.zip', '.zip')):
            self.type = 'fb2'
        elif file.lower().endswith('.epub'):
            self.type = 'epub'
        else:
            self.type = 'unknown'

    def get_authors(self, last_name_first=False):
        if last_name_first:
            new_authors = []
            authors = self.author.split(',')
            for a in authors:
                new_authors.append(format_author(a))
            return ', '.join(new_authors)
        else:
            return self.author

    def get_metadata(self, read_cover_image=False):
        if self.type == 'fb2':
            metadata = fb2meta.get_metadata(self.file, read_cover_image=read_cover_image)
            self.author = metadata['authors']
            self.author_sort = self.get_authors(last_name_first=True)
            self.title = metadata['title']
            self.description = metadata['description']
            self.lang = metadata['lang']
            self.tags = translate_tags(metadata['tags'])
            self.translator = metadata['translators']
            self.series = metadata['series']
            self.series_index = metadata['series_num']
            if read_cover_image:
                self.coverimage = metadata['coverimage']
                self.coverimage_type = metadata['coverimage_type']

        elif self.type == 'epub':
            metadata = epub_meta.get_epub_metadata(self.file, read_cover_image=read_cover_image, read_toc=False)
            self.author = ', '.join(metadata.authors)
            self.author_sort = self.get_authors(last_name_first=True)
            self.title = metadata.title
            self.description = metadata.description
            self.lang = metadata.language
            self.tags = translate_tags(metadata.subject)
            if read_cover_image:
                self.coverimage = base64.b64decode(metadata.cover_image_content)
                if metadata.cover_image_extension:
                    self.coverimage_type = metadata.cover_image_extension[1:]

        else:
            # Неизвестный формат
            pass
