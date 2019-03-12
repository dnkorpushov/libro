from libro.utils.fb2meta import Fb2Meta
from libro.utils.epubmeta import EpubMeta
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
    elif book_type == 'epub':
        epubmeta = EpubMeta(file)
        metadata = epubmeta.get_meta()

    metadata.file = file
    metadata.book_format = book_type
    return metadata
