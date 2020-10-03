#!/bin/python

import csv
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument('fold', type=int, help='the number of the fold')

args = parser.parse_args()
fold = args.fold
print(fold)

pos_file = open('pos.txt')
pos = []
for line in pos_file:
    pos.append(line)

neg_file = open('neg.txt')
neg = []
for line in neg_file:
    neg.append(line)

# print(pos[-1])


# print(len(pos))
npos = len(pos)
nneg = len(neg)

random.seed(42)
random.shuffle(pos)
random.shuffle(neg)

test_pos_size = npos / 10
test_neg_size = nneg / 10

test_pos_start = fold * test_pos_size
test_neg_start = fold * test_neg_size
test_pos_end = (fold + 1) * test_pos_size
test_neg_end = (fold + 1) * test_neg_size

test_pos = []
test_neg = []
train_pos = []
train_neg = []

for i, x in enumerate(pos):
	# if i == 0 : print(x)
	if i >= test_pos_start and i < test_pos_end:
		# print(i)
		test_pos.append(x)
	else:
		train_pos.append(x)

for i, x in enumerate(neg):
	if i >= test_neg_start and i < test_neg_end:
		test_neg.append(x)
	else:
		train_neg.append(x)

test_pos_file = open('test/pos.txt', 'w')
test_neg_file = open('test/neg.txt', 'w')
train_pos_file = open('train/pos.txt', 'w')
train_neg_file = open('train/neg.txt', 'w')

# write_facts_to_file(test_pos_file, 'autism_gene', test_pos)
# write_facts_to_file(test_neg_file, 'autism_gene', test_neg)
# write_facts_to_file(train_pos_file, 'autism_gene', train_pos)
# write_facts_to_file(train_neg_file, 'autism_gene', train_neg)
test_pos_file.writelines(test_pos)
test_neg_file.writelines(test_neg)
train_pos_file.writelines(train_pos)
train_neg_file.writelines(train_neg)

