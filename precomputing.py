
import os
from mykanren import var, facts, Relation, run

def precompute(precomp_rule_f, fact_rels):
    # precomp_rules = list(open(precomp_rule_f))
    # print(precomp_rules)
    # print(eval("".join(precomp_rules)))
    # __import__()
    _locals = globals()
    _locals.update(locals())

    if not os.path.exists(precomp_rule_f):
        return _locals['fact_rels']

    new_fact_rels = {}
    for relname, rel in fact_rels.items():
        print('defining relation', relname, 'to _locals')
        # exec('%s = Relation()' % relname, globals(), _locals)
        exec('%s = fact_rels["%s"]' % (relname, relname), globals(), _locals)
        eval('print(%s)' % relname, _locals)
    exec(open(precomp_rule_f).read(), _locals)
    # return new_fact_rels
    # return fact_rels
    return _locals['fact_rels']

def count_binding_set(args, goals, fact_rels):
    # print(friends.facts)
    bs = run(0, args, *goals)
    # print('binding set', bs)
    return len(bs)

def func2facts(rel_func, args_list, fact_rels):
    rel = rel_func.__name__
    if rel not in fact_rels:
        fact_rels[rel] = Relation(rel)
    for args in args_list:
        ret = rel_func(*args)
        fact_rels[rel].add_fact(*args, ret)


