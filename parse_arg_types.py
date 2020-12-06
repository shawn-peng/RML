
# arg types definition should in this format:
# <REL>(<ARG_TYPE_NAME>: <ARG_TYPE>, [ <ARG_TYPE_NAME>: <ARG_TYPE>, ]*)

import re


type_regex = '(?P<type>id|continuous|nominal|ordinal)'

argtype_regex = '(?P<argtype_name>\w+):\s*%s' % type_regex

arglist_regex = '(?P<arglist>%s(,\s*%s)*)' % (argtype_regex, argtype_regex)

typedef_regex = '(?P<rel_name>\w+)\(%s\)' % arglist_regex
typedef_regex = re.compile(typedef_regex)

arglist_regex = re.compile(arglist_regex)

argtype_regex = re.compile(argtype_regex)

type_regex = re.compile(type_regex)


def parse_type(typestr):
    return

def parse_argtype(argstr):
    return

def parse_reltype(reltype_str):
    m = typedef_regex.match(reltype_str)

    rel_name = m.group('rel_name')
    argtypes = m.group('arglist')
    argtypes = [(m.group('argtype_name'), m.group('type')) for m in arglist_regex.finditer(argtypes)]
    print(argtypes)
    return rel_name, argtypes

def parse_rel_types(argtypes_file):
    argtypes_file = open(argtypes_file)
    rel_types = {}
    for line in argtypes_file:
        line = line.rstrip()
        if not line:
            continue
        rel, argtypes = parse_reltype(line)
        rel_types[rel] = argtypes

    return rel_types



