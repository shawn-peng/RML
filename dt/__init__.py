
from mykanren import var, conde, conda
from mykanren import Relation, facts
from tree import Tree_Node_LChild, Tree_Node_RChild, Tree_Leaf, Tree_Root, Tree_Node_Child, Tree_Node_Parent

Decision_Node_Test = Relation()
Decision_Tree_Root = Relation()

Decision_Answer_Node = Relation()

def Decision_Node(dnode, test, tnode, fnode):
    # test1, test2, tnode1, tnode2, fnode1, fnode2 = vars(6)
    # ans = var()
    # print(dnode)
    return conde(
        # ((Decision_Answer_Node, dnode, ans), eq(test, None), eq(tnode, None), eq(fnode, None),),
        # ((Decision_Answer_Node, dnode, ans), ),
        ((Tree_Leaf, dnode), ),
        # (Tree_Node_LChild(dnode, tnode), Tree_Node_RChild(dnode, fnode), Test(test), Decision_Node_Test(dnode, test),
        #  Decision_Node(tnode,test1,tnode1,fnode1), Decision_Node(fnode,test2,tnode2,fnode2),),
        # (Tree_Node_LChild(dnode, tnode), Tree_Node_RChild(dnode, fnode), Decision_Node_Test(dnode, test),),
        ((Tree_Node_LChild, dnode, tnode), (Tree_Node_RChild, dnode, fnode), (Decision_Node_Test, dnode, test),),
    )

Decision_Node_Example = Relation()
Decision_Node_Positive = Relation()
Decision_Node_Negative = Relation()

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

# def Test_Pass(test, example):
#     return test(example)
# def Test_Fail(test, example):
#     return

def Decision_Tree_Answer(dtree, example, answer):
    root = var()
    return conde((Tree_Root(dtree, root), Decision_Node_Answer(root, example, answer),))




