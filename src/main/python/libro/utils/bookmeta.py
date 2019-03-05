from libro.utils.util import format_pattern


class Author:
    first_name = ''
    middle_name = ''
    last_name = ''

    def init(self, first_name, middle_name, last_name):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name


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
    book_format = ''
    date = ''
    cover_image_name = ''
    cover_image_data = None
    file = ''

    def get_tag_string(self):
        return ', '.join(self.tag)

    def set_tag_from_string(self, tag_string):
        self.tag = tag_string.strip().split(',')

    def set_author_from_string(self, author_string):
        self.author = self._set_person_from_string(author_string)

    def set_translator_from_string(self, translator_string):
        self.translator = self._set_person_from_string(translator_string)

    def _set_person_from_string(self, person_string):
        person_dest = []
        if person_string is not None and len(person_string) > 0:
            person_array = person_string.split(',')
            for p in person_array:
                person_elements = p.strip().split()
                person = Author()
                if len(person_elements) == 3:
                    person.first_name = person_elements[0]
                    person.middle_name = person_elements[1]
                    person.last_name = person_elements[2]
                elif len(person_elements) == 2:
                    person.first_name = person_elements[0]
                    person.last_name = person_elements[1]
                else:
                    person.last_name = p.strip()
                person_dest.append(person)

        return person_dest

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
