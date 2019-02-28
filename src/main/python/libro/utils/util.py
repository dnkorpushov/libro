

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


if __name__ == '__main__':
    fmt = format_pattern('#author, {(#series {#padnumber}) }#title{ (пер. #translator)}', [
                    ('#title', 'Понедельник начинается в субботу'),
                    ('#A', 'С'),
                    ('#author', 'Стругацкие Аркадий и Борис'),
                    ('#series', 'Фантастика'),
                    ('#padnumber', '02'),
                    ('#translator', 'Иванов')])
    print(fmt + '.fb2.zip')