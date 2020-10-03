#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 15:27:15 2019

@author: yisupeng
"""
import csv
from utils import *
import numpy as np
import random

random.seed(42)


#%%
datafile = open('iris.data')
data = csv.reader(datafile, delimiter=',')

fields = ['sl','sw','pl','pw','class']
classes = set()
examples = []
idn = 0
for row in data:
    if (len(row) == 0):
        continue
    obj = 'o%d'%idn
    sl = float(row[0])
    sw = float(row[1])
    pl = float(row[2])
    pw = float(row[3])
    c = row[4]
    classes.add(c)
    examples.append((obj, sl,sw,pl,pw, c))
    idn += 1

#random.shuffle(examples)

#%% utils
def get_list_at(l,idx):
    ret = []
    for e in l:
        ret.append(e[idx])
    return ret

def discretize(l, n):
    s = min(l)
    e = max(l)
    r = e - s
    step = r / n
    ret = []
    bins = np.arange(s,e,step)
    return np.digitize(l, bins)
        

#%%
objs = get_list_at(examples, 0)

sls = get_list_at(examples, 1)

sws = get_list_at(examples, 2)

pls = get_list_at(examples, 3)

pws = get_list_at(examples, 4)

sls = discretize(sls, 10)

sws = discretize(sws, 10)

pls = discretize(pls, 10)

pws = discretize(pws, 10)


facts = open('train/facts.txt', 'w')

for t in zip(objs, sls):
    write_fact(facts, 'sl("%s", %d).', t)
for t in zip(objs, sws):
    write_fact(facts, 'sw("%s", %d).', t)
for t in zip(objs, pls):
    write_fact(facts, 'pl("%s", %d).', t)
for t in zip(objs, pws):
    write_fact(facts, 'pw("%s", %d).', t)

facts.close()

#%%
posfile = open('pos.txt', 'w')
negfile = open('neg.txt', 'w')

for t in zip(get_list_at(examples, 5), objs):
    for c in classes:
        if c == t[0]:
            write_fact(posfile, '%s("%s").', (c,t[1]))
        else:
            write_fact(negfile, '%s("%s").', (c,t[1]))

posfile.close()
negfile.close()



