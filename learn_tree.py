
from dt import Tree_Root, Tree_Leaf, Tree_Node_Child, Tree_Node_LChild, Tree_Node_RChild, Tree_Node_Parent, \
    Decision_Node, Decision_Answer_Node, Decision_Node_Test, Decision_Node_Answer, Decision_Tree_Answer, \
    Decision_Node_Example, Decision_Node_Positive, Decision_Node_Negative

from mykanren import var, Relation, run, fact, facts, lall, lany, reify, Stream

from collections import defaultdict
import itertools
from functools import partial
import numpy as np
import heapq
import random
from graphviz import Digraph

from typing import List

class DecisionNode:
    def __init__(self, nodeid):
        self.nodeid = nodeid
        self.examples = None
        self.pos = None
        self.neg = None
        self.test = None
        pass
all_nodes = defaultdict(DecisionNode)

class BoostingTreesModel:
    def __init__(self, rels : List[Relation], pos, neg, config):
        self.rels = rels
        self.target = config.target
        self.split_times = config.split_times
        self.node_size = config.node_size
        self.modes = config.modes

        self.pos_rels = pos
        self.neg_rels = neg

        self.num_splits = 0

        self.nodes = []

        self.target_typed_vars = defaultdict(list)
        for mode in self.modes:
            rel, arg_types = mode
            if rel == self.target:
                self._add_target_vars(arg_types)
                # self.target_argtypes = (typename for guide, typename in arg_types)
                self.target_argtypes = arg_types
                del mode
                self.target_args = next(self._get_args(arg_types, self.target_typed_vars))
                print('target_args', (self.target_args))
                break

        self.pos_goal = self.pos_rels[self.target](*self.target_args)
        self.neg_goal = self.neg_rels[self.target](*self.target_args)

        self.examples = self.get_examples(self.pos_rels, self.target)
        self.examples += self.get_examples(self.neg_rels, self.target)
        print('examples', self.examples)

    tree_counts = defaultdict(int)
    def _new_tree_id(self, target):
        self.tree_counts[target] += 1
        return target+".tree_"+str(self.tree_counts[target])

    node_counts = defaultdict(int)
    def _new_node_id(self, tree_id):
        self.node_counts[tree_id] += 1
        return tree_id+".node_"+str(self.node_counts[tree_id])

    # typed_vars = defaultdict(list)
    # target_argtypes = ()
    def _add_target_vars(self, arg_types):
        for guide, typename in arg_types:
            newvar = 'Var_' + typename + '_' + str(len(self.target_typed_vars[typename]))
            newvar = var(newvar)
            self.target_typed_vars[typename].append(newvar)

    # def _add_var(self, typename, var, typed_vars):
    #     typed_vars[typename].append(var)

    def _get_args(self, arg_types, typed_vars):
        arg_lists = []
        for argpos, (guide, typename) in enumerate(arg_types):
            if guide == '+':
                exist_vars = typed_vars[typename]
                arg_lists.append(exist_vars)
            elif guide == '-':
                newvar = 'Var_' + typename + '_' + str(len(typed_vars[typename]))
                newvar = var(newvar)
                arg_lists.append([newvar])
            elif guide == '#':
                values = self._collect_type_values(typename)
                arg_lists.append(values)

        print('arg_lists', arg_lists)

        return itertools.product(*arg_lists)

    type_value_collections = defaultdict(set)
    def _collect_type_values(self, typename):
        if typename in self.type_value_collections:
            return self.type_value_collections[typename]
        collection = self.type_value_collections[typename]
        for mode in self.modes:
            rel, arg_types = mode
            for argpos, (guide, tn) in enumerate(arg_types):
                if tn == typename:
                    collection.update(self.rels[rel].get_values(argpos))
        return collection

    def get_examples(self, example_set, target):
        # x = var()
        # l = run(0, x, example_set[target](x))
        # return l
        g = example_set[target](*self.target_args)
        return list(g({}))

    # def get_node_examples(self, node):
    #     x = var()
    #     l = run(0, x, Decision_Node_Example(node, x))
    #     return l
    #def get_

    # def get_node_ex_subs(self, rel, node):
    #     #g = Decision_Node_Example(node, *self.target_args)
    #     g = rel(node, *self.target_args)
    #     return g({})

    def try_test(self, node, test, examples):
        rel, args = test

        left = []
        right = []

        # examples = self.get_node_ex_subs(Decision_Node_Example, node)
        #examples = run(1, examples, Decision_Node_Example(node, examples))[0]

        g = rel(*args)
        for s in examples:
            newss = Stream(g(s))
            if not newss.empty():
                left.append(next(newss))
            else:
                right.append(s)

        print('left', left)
        print('right', right)

        lpos = []
        lneg = []
        lunknown = []
        for s in left:
            pos_ss = self.pos_goal(s)
            neg_ss = self.neg_goal(s)
            if next(pos_ss, None):
                lpos.append(s)
            elif next(neg_ss, None):
                lneg.append(s)
            else:
                lunknown.append(s)

        print('lpos', len(lpos), lpos)
        print('lneg', len(lneg), lneg)
        print('lunknown', lunknown)

        rpos = []
        rneg = []
        runknown = []
        for s in right:
            pos_ss = self.pos_goal(s)
            neg_ss = self.neg_goal(s)
            if next((s for s in pos_ss), None):
                rpos.append(s)
            elif next((s for s in neg_ss), None):
                rneg.append(s)
            else:
                runknown.append(s)


        print('rpos', len(rpos), rpos)
        print('rneg', len(rneg), rneg)
        print('runknown', runknown)

        lscore = self.gini_score(len(lpos), len(lneg))
        rscore = self.gini_score(len(rpos), len(rneg))
        print('gini_scores', (lscore, rscore))

        l = np.log((len(left)+1, len(right)+1))
        if l.sum():
            w = l / l.sum()
            score = np.dot(w, (lscore, rscore))
        else:
            score = 1
        print('weighted avg score', score)

        return (score, (left, (lpos, lneg)), (right, (rpos, rneg)))

    # def calc_node_score(self, node):
    #     pass

    @staticmethod
    def gini_score(n1, n2):
        s = n1 + n2
        if s == 0:
            return 0
        p1 = n1 / s
        p2 = n2 / s
        return 1 - p1**2 - p2**2

    def make_answer_node(self, node, examples):
        # Tree_Leaf(node)
        # if not examples:
        #     examples = self.get_node_ex_subs(Decision_Node_Example, node)
        pos = []
        neg = []
        unknown = []
        for s in examples:
            pos_ss = self.pos_goal(s)
            neg_ss = self.neg_goal(s)
            if next(pos_ss, None):
                pos.append(s)
            elif next(neg_ss, None):
                neg.append(s)
            else:
                unknown.append(s)

        npos = len(pos)
        nneg = len(neg)

        total = (npos+nneg)
        if total:
            p = npos / total
        else:
            p = 0.5
        answer = (p, p>0.5)
        print('answer', answer)
        fact(Decision_Answer_Node, node, answer)

    # make answer nodes at leaves
    # def make_answer_nodes(self):
    #     for node in self.nodes:
    #         ch = var()
    #         ch = run(0, ch, Tree_Node_Child(node, ch))
    #         if ch:
    #             continue
    #         self.make_answer_node(node)
    #     pass

    def learn_tree(self):
        self.tree = self.learn_tree_basic()

    def learn_tree_basic(self):
        relations = self.rels
        target = self.target
        modes = self.modes
        # tree = {} # dict of relations of a tree
        treeid = self._new_tree_id(target)
        self.rootid = self._new_node_id(treeid)

        # for ex in self.examples:
        #     fact(Decision_Node_Example, self.rootid, ex)

        # pos = list(self.pos_rels[self.target](*self.target_args)({}))
        pos = run(0, *self.target_args, self.pos_goal)
        # print('pos',pos)
        # fact(Decision_Node_Positive, self.rootid, pos)

        # neg = list(self.neg_rels[self.target](*self.target_args)({}))
        neg = run(0, *self.target_args, self.neg_goal)
        # print('neg',neg)
        # fact(Decision_Node_Negative, self.rootid, neg)

        score = self.gini_score(len(pos), len(neg))
        print('root score', score)

        expanding = [] # sorted by splitting score
        #heapq.heappush(expanding, (score, self.rootid))

        # def find_best_test():
        #     test = find_best_test()
        #     print('best test', test)
        #     pass

        def expand_node(node, typed_vars, examples, score):
            print('expanding node', node)
            print('current vars', typed_vars)
            best_score = 2
            bests = []
            test = None
            lex = None
            rex = None

            def _enum_splits(node_size, prefix_rels):
                if node_size == 0:
                    yield prefix_rels
                else:
                    for relname, arg_types in modes:
                        if relname not in relations:
                            continue
                        rel = relations[relname]

                        argss = self._get_args(arg_types, typed_vars)
                        argss = list(argss)
                        print('argss', argss)
                        for args in argss:
                            yield from _enum_splits(node_size-1, prefix_rels + [((relname, arg_types), (rel, args))])

            def _gen_splits():
                for node_size in range(1, self.node_size+1):
                    yield from _enum_splits(node_size, [])

            for split in _gen_splits():
            # for rel, arg_types in modes:
            #     print('try relation', rel)
            #     print('mode', arg_types)
                arg_types, test = zip(*split)
                print('try test', test)

                s,lex,rex = self.try_test(node, test, examples)
                print('score', s)
                choice = (s, node, typed_vars, arg_types, test, examples, lex, rex)
                # if s == 0:
                #     continue
                # elif s < best_score:
                if s < best_score:
                    print('update bests')
                    best_score = s
                    bests = [choice]
                elif s == best_score:
                    print('appending choice')
                    bests.append(choice)
                print(bests)
            # if not bests or bests[0][0] >= score:
            #     print('no valuable test')
            #     #set as leaf node
            #     self.make_answer_node(node, examples)
            #     return
            best = random.sample(bests, 1)[0]
            print('best case when expanding node', node, best)
            heapq.heappush(expanding, best)

            return

        # test: (rel, args: var instances)
        # arg_types: type for each arg var
        def split_node(node, typed_vars, arg_types, test, examples, lex, rex):
            # Decision_Node_Test(node, test)
            fact(Decision_Node_Test, node, test)

            # typed_vars = defaultdict(list)
            # typed_vars.update(typed_vars) #make a shallow copy
            typed_vars = typed_vars.copy() #make a shallow copy
            print('type_vars copy:', typed_vars)
            def _add_var(typename, var):
                # if typename not in typed_vars:
                #     typed_vars[typename] = [var]
                typed_vars[typename] = typed_vars[typename] + [var] #build new list

            # add new vars
            for rel, args in test:
                for i, arg in enumerate(args):
                    guide, typename = arg_types[i]
                    print(i, arg, guide, typename)
                    if guide == '-':
                        _add_var(typename, arg)

            l = self._new_node_id(treeid)
            fact(Tree_Node_LChild, node, l)
            lex, (lpos, lneg) = lex
            # fact(Decision_Node_Example, l, lex)
            # fact(Decision_Node_Positive, l, lpos)
            # fact(Decision_Node_Negative, l, lneg)
            # for ex in map(partial(reify, self.target_args), lex):
            #     # print('ex', ex)
            #     fact(Decision_Node_Example, l, *ex)

            expand_node(l, typed_vars, lex, score)
            self.nodes.append(l)

            r = self._new_node_id(treeid)
            fact(Tree_Node_RChild, node, r)
            rex, (rpos, rneg) = rex
            # fact(Decision_Node_Example, r, rex)
            # fact(Decision_Node_Positive, r, rpos)
            # fact(Decision_Node_Negative, r, rneg)
            # for ex in map(partial(reify, self.target_args), rex):
            #     fact(Decision_Node_Example, r, *ex)

            expand_node(r, typed_vars, rex, score)
            self.nodes.append(r)

            self.num_splits += 1

        expand_node(self.rootid, self.target_typed_vars, self.examples, score)

        c = 0
        while expanding and self.num_splits < self.split_times:
            # _, node, test, lex, rex = heapq.heappop(expanding)
            # print(node, test, lex, rex)
            score, *expand = heapq.heappop(expanding)
            print('expanding', *expand)
            # split_node(node, test, lex, rex)
            split_node(*expand)
            self.print_tree(self.rootid)
            # c+=1
            # if c == 5:
            #     break

        # make answer nodes at leaves, which are what left in the expanding queue
        while expanding:
            score, *expand = heapq.heappop(expanding)
            node, arg_types, typed_vars, test, examples, lex, rex = expand
            self.make_answer_node(node, examples)


        return treeid

    def print_answer_node(self, node):
        ans = var()
        ans = run(1, ans, Decision_Answer_Node(node, ans))
        print(node, 'Answer:', ans)

    def print_tree(self, node):
        # print(node)
        t = var()
        t = run(1, t, Decision_Node_Test(node, t))
        if not t:
            self.print_answer_node(node)
            return
        print('Test for node', node, t)
        l = var()
        l = run(1, l, Tree_Node_LChild(node, l))
        if l:
            print(node, '-L->', l)
            self.print_tree(l[0])
        r = var()
        r = run(1, r, Tree_Node_RChild(node, r))
        if r:
            print(node, '-R->', r)
            self.print_tree(r[0])

    def quote_node(self, node):
        print(node)
        return node
        #return '"%s"'%  # dot.node(self.quote_node(node), str(label))

    def dot_node(self, dot, node, label):
        dot.node(self.quote_node(node), str(label))

    def dot_edge(self, dot, node, target):
        dot.edge(self.quote_node(node), self.quote_node(target))

    def dot_add_answernode(self, dot, node):
        ans = var()
        ans = run(1, ans, Decision_Answer_Node(node, ans))[0]
        # dot.node(self.quote_node(node), "%.3f: %s"%ans)
        self.dot_node(dot, node, "%.3f: %s"%ans)

    def dot_add_subtree(self, dot, node):
        t = var()
        t = run(1, t, Decision_Node_Test(node, t))
        if not t:
            self.dot_add_answernode(dot, node)
            return
        #dotnode = self.quote_node(node)
        print('t', t)
        t = t[0]
        # dot.node(node, str(t))
        self.dot_node(dot, node, t)
        l = var()
        l = run(1, l, Tree_Node_LChild(node, l))[0]
        if l:
            print('l', l)
            # dot.edge(dotnode, l)
            self.dot_edge(dot, node, l)
            self.dot_add_subtree(dot, l)
        r = var()
        r = run(1, r, Tree_Node_RChild(node, r))[0]
        if r:
            # dot.edge(dotnode, r)
            self.dot_edge(dot, node, r)
            self.dot_add_subtree(dot, r)

    def output_dot_tree(self, filename):
        dot = Digraph(comment='The Decision Tree')
        self.dot_add_subtree(dot, self.rootid)
        dot.render(filename=filename, format='pdf', view=True)
        print(dot.source)

