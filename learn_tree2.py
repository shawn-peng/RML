
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
    def __init__(self, rels : List[Relation], target, modes, pos, neg):
        self.rels = rels
        self.target = target
        self.modes = modes

        self.pos_rels = pos
        self.neg_rels = neg

        self.target_typed_vars = defaultdict(list)
        for mode in modes:
            rel, arg_types = mode
            if rel == target:
                self._add_target_vars(arg_types)
                # self.target_argtypes = (typename for guide, typename in arg_types)
                self.target_argtypes = arg_types
                del mode
                self.target_args = next(self._get_args(arg_types, self.target_typed_vars))
                print('target_args', (self.target_args))
                break

    def _add_target_vars(self, arg_types):
        for guide, typename in arg_types:
            newvar = 'Var_' + typename + '_' + str(len(self.target_typed_vars[typename]))
            newvar = var(newvar)
            self.target_typed_vars[typename].append(newvar)

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


    def learn_tree(self):
        tree = self.learn_tree_basic()

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
            for rel, arg_types in modes:
                if rel not in relations:
                    continue
                rel = relations[rel]
                print('try relation', rel)
                print('mode', arg_types)
                argss = self._get_args(arg_types, typed_vars)
                argss = list(argss)
                print('argss', argss)
                for args in argss:
                    test = (rel, args)
                    print('args', args)
                    #node_ex_ss = self.get_node_ex_subs(node)
                    #s,lex,rex = self.score_test(test, node_ex_ss)
                    s,lex,rex = self.try_test(node, test, examples)
                    print('score', s)
                    choice = (s, node, arg_types, typed_vars, test, lex, rex)
                    if s == 0:
                        continue
                    elif s < best_score:
                        print('update bests')
                        best_score = s
                        bests = [choice]
                    elif s == best_score:
                        print('appending choice')
                        bests.append(choice)
                    print(bests)
            if not bests or bests[0][0] >= score:
                print('no valuable test')
                #set as leaf node
                self.make_answer_node(node, examples)
                return
            best = random.sample(bests, 1)[0]
            print('best case when expanding node', node, best)
            heapq.heappush(expanding, best)
            return



















