# from mykanren import success, fail
from mykanren import run, eq, membero, Var, var, vars, conde
from mykanren import Relation, fact, facts, unifiable
from mykanren.assoccomm import associative, commutative
from mykanren.core import EarlyGoalError
from mykanren.arith import lor
from mykanren.util import intersection, evalt

from temp_dict import temp_dict, temp_assoc

from unification import unify, reify, isvar, hasrange, RangedVar, RealRange

from toolz import merge

import numbers
from numbers import Number
# import numpy as np

_Number = Relation()
class RegisteringRelation(Relation):
    # def __new__(cls, *args, **kwargs):
    #     return Relation(*args, **kwargs)
    def add_fact(self, *inputs):
        for x in inputs:
            if isinstance(x, numbers.Number):
                fact(_Number, x)
        Relation.add_fact(self, *inputs)

    # @classmethod
    # def gen_facts(cls):
    #     x = var()
    #     nums = run(0, x, _Number(x))
    #     nums = sorted(nums, reverse=True)
    #     print('all nums', nums)
    #     n = len(nums)
    #     for i in range(n):
    #         for j in range(i, n):
    #             fact(ge, nums[i], nums[j])
    #             if (i != j):
    #                 fact(lt, nums[j], nums[i])


class BypassingRelation(RegisteringRelation):
    def __init__(self, op, *args, **kwargs):
        self.op = op
        RegisteringRelation.__init__(self, *args, **kwargs)
    def __call__(self, *args):
        """ Returns an evaluated (callable) goal, which returns a list of
        substitutions which match args against a fact in the knowledge base.

        *args: the goal to evaluate. This consists of vars and values to
               match facts against.
        """

        def goal(substitution):
            args2 = reify(args, substitution)
            subsets = [self.index[key] for key in enumerate(args)
                       if key in self.index]
            if subsets:  # we are able to reduce the pool early
                facts = intersection(*sorted(subsets, key=len))
            else:
                facts = self.facts

            for fact in facts:
                unified = unify(fact, args2, substitution)
                if unified != False:
                    yield merge(unified, substitution)

        for x in args:
            if isvar(x):
                return goal

        return self.op(*args)


# _gt = RegisteringRelation()
# _lt = RegisteringRelation()
#
#
# def gt(x, y):
#     """ x > y """
#     if not isvar(x) and not isvar(y):
#         return eq(x > y, True)
#     else:
#         return (_gt, x, y)
#
# def lt(x, y):
#     """ x > y """
#     if not isvar(x) and not isvar(y):
#         return eq(x < y, True)
#     else:
#         return (_lt, x, y)
#
# _ge = lor(gt, eq)
# _le = lor(lt, eq)

class NumOrderRelation(Relation):
    def __init__(self, funcrel, name=None):
        Relation.__init__(self, name)
        self.funcrel = funcrel
    def __call__(self, x, y):
        return self.funcrel(x, y)

def _gt(x, y):
    # def range_gt(u):
    #     return
    def goal(substitution):
        newx, newy = reify((x, y), substitution)
        def apply_constrain(oldvar, newvar):
            if hasrange(oldvar):
                newvar = RangedVar.new_from_intersection(oldvar, newvar)
                if newvar:
                    yield temp_assoc(substitution, oldvar, newvar)
            else:
                yield temp_assoc(substitution, oldvar, newvar)

        if isvar(newx):
            if isvar(newy):
                raise EarlyGoalError('two vars in comparison')
            elif isinstance(newy, Number):
                oldvar = newx
                newvar = RangedVar(RealRange([(newy, torch.inf)]))
                yield from apply_constrain(oldvar, newvar)
            else:
                raise EarlyGoalError('Invalid constant type')
        elif isinstance(newx, Number):
            if isvar(newy):
                oldvar = newy
                newvar = RangedVar(RealRange([(-torch.inf, newx)]))
                yield from apply_constrain(oldvar, newvar)
            elif isinstance(newy, Number):
                if newx > newy:
                    yield substitution
            else:
                raise EarlyGoalError('Invalid constant type')
        else:
            raise EarlyGoalError('Invalid constant type')
    return goal

def _lt(x, y):
    # def range_gt(u):
    #     return
    def goal(substitution):
        newx, newy = reify((x, y), substitution)
        # merge constrains of 2 vars, add mapping from old var to new var
        # new var has intersection range
        def apply_constrain(oldvar, newvar):
            if hasrange(oldvar):
                newvar = RangedVar.new_from_intersection(oldvar, newvar)
                if newvar:
                    yield temp_assoc(substitution, oldvar, newvar)
            else:
                yield temp_assoc(substitution, oldvar, newvar)

        # print("x:", x)
        # print("y:", y)

        if isvar(newx):
            if isvar(newy):
                raise EarlyGoalError('two vars in comparison')
            elif isinstance(newy, Number):
                oldvar = newx
                newvar = RangedVar(RealRange([(newy, torch.inf)]))
                yield from apply_constrain(oldvar, newvar)
            else:
                raise EarlyGoalError('Invalid constant type')
        elif isinstance(newx, Number):
            if isvar(newy):
                oldvar = newy
                newvar = RangedVar(RealRange([(-torch.inf, newx)]))
                yield from apply_constrain(oldvar, newvar)
            elif isinstance(newy, Number):
                if newx < newy:
                    yield substitution
            else:
                raise EarlyGoalError('Invalid constant type')
        else:
            raise EarlyGoalError('Invalid constant type')
    return goal

gt = NumOrderRelation(_gt, 'gt')
lt = NumOrderRelation(_lt, 'gt')

ge = gt

le = lt

# gt = BypassingRelation(torch.greater)
# ge = BypassingRelation(torch.greater_equal)
# lt = BypassingRelation(torch.less)
# le = BypassingRelation(torch.less_equal)

# complimentary = Relation()
# facts(complimentary,
#       (ge, lt),
#       (gt, le))

# def neg(x, *args):
#     # x = args[0]
#     if isinstance(x, Relation):
#         rel = x
#         nrel = var()
#         ans = run(1, nrel, (complimentary, rel, nrel))
#         if not ans:
#             print('in neg, relation results', run(0, nrel, (rel, *args)))
#             return (neg, rel(*args))
#         else:
#             nrel = ans[0]
#             return (nrel, *args)
#         # return (conde,
#         #         ((complimentary, rel, nrel), (nrel, *args)),
#         #         ()
#     elif isvar(x):
#         raise EarlyGoalError()
#     elif callable(x):
#         f = x
#         try:
#             return (neg, f(*args))
#         except Exception as e:
#             print(e)
#             raise EarlyGoalError(e)
#     elif isinstance(x, tuple):
#         term = x
#         term = evalt(term)
#         return (neg, term, *args)
#     else:
#         return not x

class NumberVar(Var):
    def __new__(cls, *token):
        obj = Var(*token)
        return obj

# def Number(x):
#     fact(_Number)
#     if isinstance(x, Var):
#         return (NumberVar, x)
#     else:
#         return isinstance(x, numbers.Number)

# fact(Number, x)

def count(x, n):
    def goal(s):
        pass



