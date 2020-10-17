
from mykanren import var, facts, Relation, run

def precompute(precomp_rule_f, fact_rels):
    # precomp_rules = list(open(precomp_rule_f))
    # print(precomp_rules)
    # print(eval("".join(precomp_rules)))
    # __import__()
    _locals = locals()
    new_fact_rels = {}
    for relname, rel in fact_rels.items():
        print('defining relation', relname, 'to _locals')
        # exec('%s = Relation()' % relname, globals(), _locals)
        exec('%s = fact_rels["%s"]' % (relname, relname), globals(), _locals)
        eval('print(%s)' % relname, globals(), _locals)
    exec(open(precomp_rule_f).read(), globals(), _locals)
    # return new_fact_rels
    # return fact_rels
    return _locals['fact_rels']

# def count

def func2facts(rel_func, args_list, fact_rels):
    for args in args_list:
        ret = rel_func(*args)
        fact_rels[rel_func.name].add_fact(*ret)
