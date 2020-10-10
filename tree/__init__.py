
from mykanren import var, conde, conda
from mykanren import Relation, facts

Tree = Relation()
Tree_Root = Relation()
Tree_Node_LChild = Relation()
Tree_Node_RChild = Relation()
Tree_Leaf = Relation()
# Tree_Node_Null = Relation()

# facts(Tree_Node_LChild,
#       ('a', 'b'),
#       ('b', 'd'))
# facts(Tree_Node_RChild,
#       ('a', 'c'),
#       ('b', 'e'))

def Tree_Node_Child(node, cnode):
    return conde(
        (Tree_Node_LChild(node, cnode),),
        (Tree_Node_RChild(node, cnode),)
    )

def Tree_Node_Parent(node, pnode):
    return Tree_Node_Child(pnode, node)

# def Tree_Node_Leaf(node):


