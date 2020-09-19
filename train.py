import os
import sys
import json


from parsing_facts import parse_facts
from learn_tree import BoostingTreesModel

from parse_modes import parse_modes

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
        self.modes = modes


conf = Config(sys.argv[1])

proj_dir = conf.proj_dir

train_facts = proj_dir + 'train/facts.txt'
train_facts = open(train_facts)

pos = proj_dir + 'train/pos.txt'
pos = open(pos)
pos_rel = parse_facts(pos)
print(pos_rel)

neg = proj_dir + 'train/neg.txt'
neg = open(neg)
neg_rel = parse_facts(neg)
print(neg_rel)

#def train(train_facts):
relations = parse_facts(train_facts)
common_rels = {
    'gt': gt,
    'lt': lt,
}
relations.update(common_rels)
# model_conf = {}

sys.path.append(proj_dir)
import precomputes

precomp_rels = precompute(proj_dir + 'precomputes.py', relations)

# tree = learn_tree(relations, conf['target'], modes)
model = BoostingTreesModel(relations, pos_rel, neg_rel, conf)
tree = model.learn_tree()
model.output_dot_tree('classification_tree')


