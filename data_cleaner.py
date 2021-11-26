import re

import unidecode

CLEANER_RE = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')


def remove_html(input_data, data_key):
    out_data = dict()
    for key, val in input_data.items():
        if key == data_key:
            clean_val = re.sub(CLEANER_RE, '', val)
            out_data[key] = unidecode.unidecode(clean_val)
        else:
            out_data[key] = val
    return out_data
