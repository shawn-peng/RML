import os
import sys
import json


from parsing_facts import parse_facts
from learn_tree import BoostingTreesModel

from parse_modes import parse_modes
from parse_type_def import parse_type_def

from tensorkanren.types import VarType

from numsys.number_relations import gt, lt

from precomputing import *


class Config:
    def __init__(self, config_file):
        conf = open(config_file)
        conf = json.load(conf)

        self.proj_dir = conf['proj_dir']

        modes = self.proj_dir + 'modes.txt'
        modes = parse_modes(modes)
        print(modes)

        self.target = conf['target']
        self.split_times = conf['num_splits']
        self.precomputing = conf['precomputing'] if 'precomputing' in conf else False
        self.modes = modes

        var_types = self.proj_dir + 'type_def.txt'
        var_types = parse_type_def(var_types)
        print(var_types)

        self.var_types = []
        for t in var_types.items():
            print(t)
            self.var_types.append(VarType(*t))

        # rel_types = self.proj_dir + 'rel_types.txt'
        # rel_types = parse_rel_types
        rel_types = {}
        for rel, arglist in modes:
            # rel_types[rel] = [argtype for _, argtype in arglist]
            rel_types[rel] = list(zip(*arglist))[1] # equivalent as above
        rel_types = {rel: list(map(lambda typename: VarType.get_type(typename), arglist)) for rel, arglist in rel_types.items()}
        self.rel_types = rel_types



conf = Config(sys.argv[1])

proj_dir = conf.proj_dir

train_facts = proj_dir + 'train/facts.txt'
train_facts = open(train_facts)

pos = proj_dir + 'train/pos.txt'
pos = open(pos)
pos_rel = parse_facts(pos, conf.rel_types)
print(pos_rel)

neg = proj_dir + 'train/neg.txt'
neg = open(neg)
neg_rel = parse_facts(neg, conf.rel_types)
print(neg_rel)

#def train(train_facts):
relations = parse_facts(train_facts, conf.rel_types)
common_rels = {
    'gt': gt,
    'lt': lt,
}
relations.update(common_rels)
# model_conf = {}

sys.path.append(proj_dir)

if conf.precomputing:
    precomp_rels = precompute(proj_dir + 'precomputes.py', relations)
    print('precomp rels', precomp_rels)
    print('rels', relations)
    print('num smoking friends', relations['num_of_smoking_friends'].facts)
    # exit()

# tree = learn_tree(relations, conf['target'], modes)
model = BoostingTreesModel(relations, pos_rel, neg_rel, conf)
tree = model.learn_tree()
model.output_dot_tree('classification_tree')


