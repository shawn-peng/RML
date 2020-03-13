from .dispatch import dispatch
from .variable import Var

from .value_space import RealRange
from temp_dict import *


# @unifiable
class RangedVar(Var):
    """ Logic Variable """

    def __new__(cls, range=None, *token):
        if len(token) == 0:
            token = "_%s" % Var._id
            Var._id += 1
        elif len(token) == 1:
            token = token[0]

        obj = object.__new__(cls)
        obj.token = token

        if range is None:
            range = RealRange()
        obj.range = range# RealRange(range)
        # obj.range = range #RealRange()
        return obj

    def __str__(self):
        return "~" + str(self.token) + "(%s)"%self.range
    __repr__ = __str__

    def __eq__(self, other):
        return type(self) == type(other) and self.token == other.token

    def __hash__(self):
        return hash((type(self), self.token))

    @classmethod
    def new_from_intersection(cls, a, b):
        return cls.__new__(cls, range=a.range & b.range)

    def unify(self, other):
        # assert(hasrange(other))
        if hasrange(other):
            new_range = self.range & other.range
            self.range = new_range
            other.range = new_range
            return bool(new_range)
        else:
            return other in self.range



var = lambda *args: Var(*args)
vars = lambda n: [var() for i in range(n)]


def hasrange(x):
    return isinstance(x, RangedVar)

@dispatch(RangedVar, RangedVar, dict)
def unify(u, v, s):
    w = RangedVar.new_from_intersection(u, v)
    if w:
        s = temp_assoc(s, u, w)
        s = temp_assoc(s, v, w)
        return s
    else:
        return False
    # if u.unify(v):
    #     return s
    # else:
    #     return False

# @dispatch(RangedVar, object, dict)
# def unify(u, v, s):
#     if u.unify(v):
#         return temp_assoc(s, u, v)
#     else:
#         return False
#
# @dispatch(object, RangedVar, dict)
# def unify(u, v, s):
#     if v.unify(u):
#         return temp_assoc(s, v, u)
#     else:
#         return False


# @dispatch(RangedVar, object, dict)
# def unify(u, v, s):


# @dispatch(RangedVar)
# def isvar(v):
#     return True


# @dispatch(object)
# def isvar(o):
#     return not not _glv and hashable(o) and o in _glv


# @contextmanager
# def variables(*variables):
#     """ Context manager for logic variables
#
#     >>> from __future__ import with_statement
#     >>> with variables(1):
#     ...     print(isvar(1))
#     True
#
#     >>> print(isvar(1))
#     False
#
#     Normal approach
#
#     >>> from unification import unify
#     >>> x = var('x')
#     >>> unify(x, 1)
#     {~x: 1}
#
#     Context Manager approach
#     >>> with variables('x'):
#     ...     print(unify('x', 1))
#     {'x': 1}
#     """
#     old_global_logic_variables = _global_logic_variables.copy()
#     _global_logic_variables.update(set(variables))
#     try:
#         yield
#     finally:
#         _global_logic_variables.clear()
#         _global_logic_variables.update(old_global_logic_variables)
