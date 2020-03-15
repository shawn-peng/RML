import re

line_regex = re.compile('(.*?)(//.*)?')

def _filter_comment(line):
    it = iter(line)
    for c in it:
        if c == '/':
            c2 = next(it)
            if c2 == '/':
                return
            yield c
            yield c2
        else:
            yield c

modearg_regex = '[+\-#]\w+' #arg types are +,-,#

modearg_list_regex = '(' + modearg_regex + ')(\s*,\s*(.*))?'
modearg_list_regex = re.compile(modearg_list_regex)
def _split_args(argstr):
    if not argstr:
        return
    m = modearg_list_regex.match(argstr)
    if m is None:
        return
    yield m.group(1)
    yield from _split_args(m.group(3))

def _parse_arg(arg):
    type = arg[0]
    name = arg[1:]
    return (type, name)

def _parse_args(argstr):
    args = []
    for arg in _split_args(argstr):
        print('arg', arg)
        arg = _parse_arg(arg)
        args.append(arg)
    return args


mode_regex = '(\w+)\((' + modearg_regex + '(\s*,\s*' + modearg_regex + ')*)\)\.'
mode_regex = re.compile(mode_regex)

def _parse_mode(line):
    print("parsing", line)
    m = mode_regex.match(line)
    rel = m.group(1)
    args = m.group(2)
    # name = ''
    # for c in line:
    #     if c ==
    args = _parse_args(args)
    # print('args', args)
    return (rel, args)


def parse_modes(mode_filename):
    modes_file = open(mode_filename)

    modes = []
    for line in modes_file:
        # line = line.rstrip()
        # m = line_regex.match(line)
        # line = m.group(1).rstrip()
        line = _filter_comment(line)
        line = ''.join(line).rstrip()
        # print('line', line, not line)
        if not line:
            continue
        mode = _parse_mode(line)
        # print(mode)
        modes.append(mode)

    return modes
