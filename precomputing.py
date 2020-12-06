
import os
# import numpy as np
import tensorflow as tf
# from mykanren import var, facts, Relation, run
from tensorkanren import var, facts, Relation
from tensorkanren.variable import TypedVar
from tensorkanren.substitution import Substitution
from itertools import starmap

def precompute(precomp_rule_f, rel_types, fact_rels):
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

def compose_goals(first, *rest):
    if not rest:
        return first
    return lambda s: compose_goals(*rest)(first(s))

# count_binding_set = None
# def _count_binding_set(args, goals):
def count_binding_set(args, goals):

    # print(friends.facts)
    # bs = run(0, args, *goals)
    # print('binding set', bs)
    # return len(bs)
    args = tuple(args)
    sub = compose_goals(*goals)({})
    bs = sub.reduce(*args, op=tf.sum)
    return bs


# global count_binding_set
# count_binding_set = _count_binding_set


def encode_args(arg_types, args_list):
    def encode(args):
        return tuple(starmap(lambda t, arg: t.encode(arg), zip(arg_types, args)))
    return list(map(lambda args: encode(args), args_list))

def decode_args(arg_types, ind):
    # def decode(row):
    #     return tuple(starmap(lambda t, arg: t.encode(arg), zip(arg_types, args)))
    # [decode(row) for row in res_tensor]
    # return list(map(lambda args: encode(args), args_list))
    return tuple(starmap(lambda arg_type, i: arg_type.decode(i), zip(arg_types, ind)))


# def get_facts_from_result_tensor(res):


def args_list_to_tensor(arg_types, args_list):
    ind = encode_args(arg_types, args_list)
    ind = tuple(zip(*ind))
    shape = list(map(lambda t: t.size(), arg_types))
    res = tf.ndarray(shape, tf.bool)
    res[ind] = True
    return res

def func2facts(rel_func, rel_type, args, fact_rels):
    rel = rel_func.__name__
    # t = rel_types[rel]
    # rel_type =
    if rel not in fact_rels:
        fact_rels[rel] = Relation(rel_type, rel)
    rel = fact_rels[rel]
    # for args in args_list:
    #     ret = rel_func(*args)
    #     fact_rels[rel].add_fact(*args, ret)
    # arg_tensor = args_list_to_tensor(rel.arg_types[:-1], args_list)

    sub = Substitution({})
    # args = tuple(starmap(lambda i, arg_type: TypedVar(arg_type, 'var%d'%i), enumerate(rel_type[:-1])))
    # sub = sub.unify(arg_tensor, *args)
    res = rel_func(*args)

    print(res)
    # sub.unify(res, *args)
    arg_types = rel_type[:-1]
    res_type = rel_type[-1]
    res_type.fit(res)

    for ind in tf.argwhere(res):
        rel.add_fact(*decode_args(arg_types, ind), *res[ind])

    # res_var = TypedVar(res_type, 'res')


