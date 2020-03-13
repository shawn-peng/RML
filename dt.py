from mykanren import run, eq, membero, var, vars, conde, unify, conda
from mykanren import Relation, fact, facts, unifiable
from mykanren.util import evalt

from functools import partial

from number_relations import RegisteringRelation, BypassingRelation, ge, lt, neg

parent = Relation()

facts(parent,
      ("Homer", "Bart"),
      ("Homer", "Lisa"),
      ("Abe",  "Homer"))

x = var()

ans = run(2, x, eq(x, 5))

def grandparent(x, z):
    y = var()
    return conde((parent(x,y), parent(y,z)))

# print(ans)

# ================================================================================

from mykanren.assoccomm import eq_assoccomm as eq
from mykanren.assoccomm import commutative, associative

# Define some dummy Operationss
add = 'add'
mul = 'mul'
# Declare that these ops are commutative using the facts system
fact(commutative, mul)
fact(commutative, add)
fact(associative, mul)
fact(associative, add)

# Define some wild variables
x, y = var('x'), var('y')

# Two expressions to match
pattern = (mul, (add, 1, x), y)                # (1 + x) * y
# pattern = (mul, x, y)                        # (1 + x) * y
expr    = (mul, 2, (add, 3, 1))                # 2 * (3 + 1)
print(run(0, (x,y), eq(pattern, expr)))        # prints ((3, 2),) meaning
                                               #   x matches to 3
                                               #   y matches to 2

# Tree_Parent = Relation()
Tree_Root = Relation()
Tree_Node_LChild = Relation()
Tree_Node_RChild = Relation()

facts(Tree_Node_LChild,
      ('a', 'b'),
      ('b', 'd'))
facts(Tree_Node_RChild,
      ('a', 'c'),
      ('b', 'e'))

def Tree_Node_Child(node, cnode):
    return conde(
        (Tree_Node_LChild(node, cnode),),
        (Tree_Node_RChild(node, cnode),)
    )

def Tree_Node_Parent(node, pnode):
    return Tree_Node_Child(pnode, node)

# print(run(0, (x,y), Tree_Node_Parent(x, y)))
# print(run(0, (x,y), Tree_Node_LChild(x, y)))


# Test = Relation()
# Test takes an example as input and return a bool value as output
# def Test(test):
    # return conde((True,))
    # return callable(test)

Decision_Node_Test = Relation()
Decision_Tree_Root = Relation()

Decision_Answer_Node = Relation()

Number = Relation()

# def Decision_Node_Test(dnode, test):
    # minimize(test, SplitCost(dnode))
    # ArgMax(test, SplitGain(dnode, test))

def Decision_Node(dnode, test, tnode, fnode):
    # test1, test2, tnode1, tnode2, fnode1, fnode2 = vars(6)
    ans = var()
    # print(dnode)
    return conde(
        ((Decision_Answer_Node, dnode, ans), eq(test, None), eq(tnode, None), eq(fnode, None),),
        # (Tree_Node_LChild(dnode, tnode), Tree_Node_RChild(dnode, fnode), Test(test), Decision_Node_Test(dnode, test),
        #  Decision_Node(tnode,test1,tnode1,fnode1), Decision_Node(fnode,test2,tnode2,fnode2),),
        # (Tree_Node_LChild(dnode, tnode), Tree_Node_RChild(dnode, fnode), Decision_Node_Test(dnode, test),),
        ((Tree_Node_LChild, dnode, tnode), (Tree_Node_RChild, dnode, fnode), (Decision_Node_Test, dnode, test),),
    )

def Decision_Node_Answer(dnode, example, answer):
    # test = unifiable(Test)
    test = var()
    tnode = var()
    fnode = var()

    # return conde(
    #     # (Decision_Answer_Node(dnode, answer), (unify, test, example), )
    #     # ((Decision_Answer_Node, dnode, answer), (unify, test, example), )
    #     ((Decision_Answer_Node, dnode, answer),)
    # )
    # return conde(
    #     (Decision_Answer_Node(dnode, answer), unify(example, var())),
    #     (Decision_Node(dnode, test, tnode, fnode),
    #      conde(
    #         (True, Decision_Node_Answer(tnode,example,answer), ),
    #         (Decision_Node_Answer(fnode,example,answer), )
    #      ), )
    # )
    return conde(
        ((Decision_Answer_Node, dnode, answer), ),
        ((Decision_Node, dnode, test, tnode, fnode),
         conda(
            ((test, example), (Decision_Node_Answer, tnode, example, answer), ),
            ((Decision_Node_Answer, fnode, example, answer), )
         ), )
    )
    # ans = run(1, example, test(example))

def Test_Pass(test, example):
    return test(example)
def Test_Fail(test, example):
    return

def Decision_Tree_Answer(dtree, example, answer):
    root = var()
    return conde((Decision_Tree_Root(dtree, root), Decision_Node_Answer(root, example, answer),))


age = RegisteringRelation()

def age_ge(x, y):
    v = var()
    print(x, y)
    return (conde, ((age, x, v), (ge, v, y)))
def age_lt(x, y):
    v = var()
    return (conde, ((age, x, v), (lt, v, y)))
# valtest = Test(lambda x:x.val > 5)
# valtest = (lambda x:x.val > 5)
# x, y = vars(2)
# x = var()
facts(Decision_Node_Test,
      ('a', lambda x : age_ge(x, 18))
)

facts(Decision_Answer_Node,
      ('b', 'Up'),
      ('c', 'Down'))

#facts(Decision_Node)

fact(Decision_Tree_Root, 'dt1', 'a')

# from collections import namedtuple
# ValExample = namedtuple('ValExample', ['val'])

# ex1 = ValExample(1)
# ex2 = ValExample(10)
# print(age)
# print(isinstance(age, Relation))


facts(age,
      ('bob', 20),
      ('alice', 18),
      ('tom', 10),
      ('daniel', 20))

RegisteringRelation.gen_facts()

Example = Relation()
facts(Example,
      ('bob', ),
      ('alice', ))

ex = var()
ans = var()

a,b,c,d = vars(4)
# print(run(0, (a,b), age(a,b)))
# print(run(0, (a,b), ge(a,b)))
# print(run(0, (a,b), Decision_Answer_Node(a,b)))
# print(run(0, (a,b,c,d), Decision_Node(a,b,c,d)))
# print(run(0, (a, b), Decision_Tree_Root(a, b)))
# print(run(0, a, (age, a, 20)))
# print('age = 18 or 20', run(0, (a,b), (conda,
#                                    ((age, a, 21), (age, a, b)),
#                                    ((age, a, 18), (age, a, b))
#                                    )))
# print(run(0, (ex, ans), Example(ex), Decision_Tree_Answer('dt1', ex, ans)))
# print(run(1, (a, b, c), Decision_Node_Answer(a, b, c)))
test = run(0, (a, b), (Decision_Node, 'a', a, var(), var()))[0][0]
print('node test', test)
print('pass goal', test(b))
# print('pass eg', run(0, (b), (test(b)),))
print(run(0, (a), (conde, ((age, a, b), (ge, b, 18)))))

# x,y,z = vars(3)
# print(run(0, x, ge(x)))
# RegisteringRelation.gen_facts()
# print('values < 20')
# print(run(0, x, (neg, ge, x, 20)))









