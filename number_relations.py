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
import numpy as np

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

def gt(x, y):
    # def range_gt(u):
    #     return
    def goal(substitution):
        def apply_constrain(oldvar, newvar):
            if hasrange(oldvar):
                newvar = RangedVar.new_from_intersection(oldvar, newvar)
                if newvar:
                    yield temp_assoc(substitution, oldvar, newvar)
            else:
                yield temp_assoc(substitution, oldvar, newvar)

        if isvar(x):
            if isvar(y):
                raise EarlyGoalError('two vars in comparison')
            elif isinstance(y, Number):
                oldvar = x
                newvar = RangedVar(RealRange([(y, np.inf)]))
                yield from apply_constrain(oldvar, newvar)
            else:
                raise EarlyGoalError('Invalid constant type')
        elif isinstance(x, Number):
            if isvar(y):
                oldvar = y
                newvar = RangedVar(RealRange([(-np.inf, x)]))
                yield from apply_constrain(oldvar, newvar)
            elif isinstance(y, Number):
                if x > y:
                    yield substitution
            else:
                raise EarlyGoalError('Invalid constant type')
        else:
            raise EarlyGoalError('Invalid constant type')
    return goal

def lt(x, y):
    # def range_gt(u):
    #     return
    def goal(substitution):
        def apply_constrain(oldvar, newvar):
            if hasrange(oldvar):
                newvar = RangedVar.new_from_intersection(oldvar, newvar)
                if newvar:
                    yield temp_assoc(substitution, oldvar, newvar)
            else:
                yield temp_assoc(substitution, oldvar, newvar)

        # print("x:", x)
        # print("y:", y)

        if isvar(x):
            if isvar(y):
                raise EarlyGoalError('two vars in comparison')
            elif isinstance(y, Number):
                oldvar = x
                newvar = RangedVar(RealRange([(y, np.inf)]))
                yield from apply_constrain(oldvar, newvar)
            else:
                raise EarlyGoalError('Invalid constant type')
        elif isinstance(x, Number):
            if isvar(y):
                oldvar = y
                newvar = RangedVar(RealRange([(-np.inf, x)]))
                yield from apply_constrain(oldvar, newvar)
            elif isinstance(y, Number):
                if x < y:
                    yield substitution
            else:
                raise EarlyGoalError('Invalid constant type')
        else:
            raise EarlyGoalError('Invalid constant type')
    return goal


ge = gt

le = lt


# gt = BypassingRelation(np.greater)
# ge = BypassingRelation(np.greater_equal)
# lt = BypassingRelation(np.less)
# le = BypassingRelation(np.less_equal)

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



