from libro.utils.util import format_pattern


class BookMeta:
    id = None
    title = ''
    author = []
    series = ''
    series_index = ''
    tag = []
    description = ''
    translator = []
    lang = ''
    src_lang = ''
    format = ''
    date = ''
    publisher = ''
    cover_image_name = ''
    cover_image_data = None
    file = ''

    def get_tag_string(self):
        return ', '.join(self.tag)

    def set_tag_from_string(self, tag_string):
        self.tag = tag_string.strip().split(',')

    def set_author_from_string(self, author_string):
        self.author = author_string.split()

    def set_translator_from_string(self, translator_string):
        self.translator = translator_string.split()

    def get_author_string(self, name_format='{#f {#m }}#l', short=False, short_count=2, short_suffix=' и др'):
        return self._get_person_string(self.author, name_format=name_format,
                                       short=short, short_count=short_count, short_suffix=short_suffix)

    def get_translator_string(self, name_format='#l', short=True, short_count=1, short_suffix=''):
        return self._get_person_string(self.translator, name_format=name_format,
                                       short=short, short_count=short_count, short_suffix=short_suffix)

    def _get_person_string(self, person_list, name_format, short, short_count, short_suffix):
        def get_first_char(text):
            if text is not None and len(text) > 0:
                return text[0]
            else:
                return ''

        dest_list = []
        i = 0
        for person in person_list:
            dest_list.append(format_pattern(name_format, [('#f', person.first_name),
                                                          ('#m', person.middle_name),
                                                          ('#l', person.last_name),
                                                          ('#fi', get_first_char(person.first_name)),
                                                          ('#mi', get_first_char(person.middle_name))]))
            i += 1
            if short and i == short_count:
                break

        person_string = ', '.join(dest_list)
        if short and len(person_list) > short_count:
            person_string = person_string + short_suffix
        return person_string
