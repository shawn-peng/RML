from unification.ranged_variable import RangedVar
from unification.value_space import RealRange
from unification.core import reify, unify

x = RangedVar()
y = RangedVar(range=RealRange([(0,1)]))

print(unify(x, y, {}))
s = {y:2}
y = reify(y, s)
print(y)
print(unify(x, y, s))
print(x, y)
