from mykanren import run, eq, membero, var, conde
# from mykanren import Relation, facts
from tensorkanren import Relation, facts

import re
# import numpy as np

fact_regex = re.compile('(\w+)\((.*)\).')

#seq_first_regex = re.compile('\(')

def parse_tuple(s):
    print(s)
    tup = eval(s)
    if isinstance(tup, tuple):
        return tup
    else:
        return (tup,)
    # arg = []
    # for c in str:


def parse_fact(line):
    print(line)
    m = fact_regex.match(line)
    rel = m.group(1)
    args = m.group(2)
    args = parse_tuple(args)
    return (rel, *args)

def parse_facts(factsfile, rel_types, fact_relations = None):
    if fact_relations is None:
        fact_relations = {}
    for line in factsfile:
        line = line.rstrip()
        if not line:
            continue
        fact = parse_fact(line)
        # print(fact)
        rel, *args = fact
        # args = tuple(args)
        # print(args)
        if rel not in rel_types:
            print('skipping', rel, *args)
            continue
        if rel not in fact_relations:
            fact_relations[rel] = Relation(rel_types[rel], rel)
        rel = fact_relations[rel]
        # print(rel)
        rel.add_fact(*args)
    return fact_relations

#fact_relations = parse_facts(factsfile)
# for rel_name, rel in fact_relations.items():
#     print(rel_name, rel)
#     x = var()
#     print(run(0, x, rel(x)))

def parse_examples(examplefile, type):
    fact_relations = {}
    for line in examplefile:
        line = line.rstrip()
        if not line:
            continue
        fact = parse_fact(line)
        # print(fact)
        rel, *args = fact
        # args = tuple(args)
        # print(args)
        if rel not in fact_relations:
            fact_relations[rel] = Relation(rel)
        rel = fact_relations[rel]
        # print(rel)
        if type == 'pos':
            rel.add_fact(1e8, *args)
        elif type == 'neg':
            rel.add_fact(-1e8, *args)
        elif type == 'val':
            rel.add_fact(*args)
        else:
            raise RuntimeError('wrong example type: '+type)

    return fact_relations



