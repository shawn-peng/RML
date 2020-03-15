import os
import sys
import json

from parsing_facts import parse_facts
from learn_tree import learn_tree

from parse_modes import parse_modes

conf = open(sys.argv[1])
conf = json.load(conf)
proj_dir = conf['proj_dir']

modes = proj_dir + 'modes.txt'
modes = parse_modes(modes)
print(modes)

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
tree = learn_tree(relations, conf['target'])

