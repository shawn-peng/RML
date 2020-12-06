
# a type def is in form:
# <ARG_TYPE_NAME>: <VAL_TYPE>
# VAL_TYPE can be one of the following,
# id|continuous|nominal|ordinal

import re

type_regex = '(?P<type>id|continuous|nominal|ordinal)'

argtype_regex = '(?P<argtype_name>\w+):\s*%s' % type_regex
argtype_regex = re.compile(argtype_regex)

def parse_type_def(type_def_file):
    type_def_file = open(type_def_file)

    types = {}

    for line in type_def_file:
        line = line.rstrip()
        if not line:
            continue
        m = argtype_regex.match(line)

        typename = m.group('argtype_name')
        type = m.group('type')

        types[typename] = type

    return types

