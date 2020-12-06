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
import re
from itertools import starmap

random.seed(42)


#%%
datafile = open('agaricus-lepiota.data')
data = csv.reader(datafile, delimiter=',')

info = '''
Attribute Information: (classes: edible=e, poisonous=p)
     1. cap-shape:                bell=b,conical=c,convex=x,flat=f,
                                  knobbed=k,sunken=s
     2. cap-surface:              fibrous=f,grooves=g,scaly=y,smooth=s
     3. cap-color:                brown=n,buff=b,cinnamon=c,gray=g,green=r,
                                  pink=p,purple=u,red=e,white=w,yellow=y
     4. bruises?:                 bruises=t,no=f
     5. odor:                     almond=a,anise=l,creosote=c,fishy=y,foul=f,
                                  musty=m,none=n,pungent=p,spicy=s
     6. gill-attachment:          attached=a,descending=d,free=f,notched=n
     7. gill-spacing:             close=c,crowded=w,distant=d
     8. gill-size:                broad=b,narrow=n
     9. gill-color:               black=k,brown=n,buff=b,chocolate=h,gray=g,
                                  green=r,orange=o,pink=p,purple=u,red=e,
                                  white=w,yellow=y
    10. stalk-shape:              enlarging=e,tapering=t
    11. stalk-root:               bulbous=b,club=c,cup=u,equal=e,
                                  rhizomorphs=z,rooted=r,missing=?
    12. stalk-surface-above-ring: fibrous=f,scaly=y,silky=k,smooth=s
    13. stalk-surface-below-ring: fibrous=f,scaly=y,silky=k,smooth=s
    14. stalk-color-above-ring:   brown=n,buff=b,cinnamon=c,gray=g,orange=o,
                                  pink=p,red=e,white=w,yellow=y
    15. stalk-color-below-ring:   brown=n,buff=b,cinnamon=c,gray=g,orange=o,
                                  pink=p,red=e,white=w,yellow=y
    16. veil-type:                partial=p,universal=u
    17. veil-color:               brown=n,orange=o,white=w,yellow=y
    18. ring-number:              none=n,one=o,two=t
    19. ring-type:                cobwebby=c,evanescent=e,flaring=f,large=l,
                                  none=n,pendant=p,sheathing=s,zone=z
    20. spore-print-color:        black=k,brown=n,buff=b,chocolate=h,green=r,
                                  orange=o,purple=u,white=w,yellow=y
    21. population:               abundant=a,clustered=c,numerous=n,
                                  scattered=s,several=v,solitary=y
    22. habitat:                  grasses=g,leaves=l,meadows=m,paths=p,
                                  urban=u,waste=w,woods=d
'''

field_start_re = re.compile('\s*\d+\. ([?\w-]+):\s*(.*)')
def get_fields_desc(info):
    info = info.split('\n')[2:]
    desc = ''
    for line in info:
        if field_start_re.match(line) and desc:
            yield desc
            desc = line.strip()
        else:
            desc += line.strip()

def get_field_name(desc):
    m = field_start_re.match(desc)
    return m.group(1)
def get_field_valuemap(desc):
    m = field_start_re.match(desc)
    return {k: v for v, k in map(lambda s: (s.split('=')), m.group(2).split(','))}

def get_fields(info):
    for desc in get_fields_desc(info):
        # print(desc)
        fname = get_field_name(desc)
        fvals = get_field_valuemap(desc)
        if '?' in fname:
            fname = fname.replace('?', '')
            # fvals['?'] = '?'
        # if (len(fvals) == 2):
        #     print(fname, fvals)
        yield fname, fvals



def parse_info(info):
    # for field in get_fields(info):
    #     print(field)
    fields = list(get_fields(info))
    # print(fields)
    return fields

fields = [('class', {'e':'edible', 'p':'poisonous'})]
fields += parse_info(info)

# print(fields)

# fields = ['class','sl','sw','pl','pw']

def parse_examples(data):
    idn = 0
    for row in data:
        if (len(row) == 0):
            continue
        ex = (dict
               (starmap(lambda field_info, field_val: (field_info[0], field_info[1][field_val]), zip(fields, row))))
        obj = 'o%d' % idn
        ex = (obj, ex)
        yield ex
        idn += 1

# classes = set()
examples = list(parse_examples(data))

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

import os
def mkdir(d):
    if not os.path.exists(d):
        os.mkdir(d)
mkdir('train')
mkdir('test')

facts = open('train/facts.txt', 'w')
posfile = open('pos.txt', 'w')
negfile = open('neg.txt', 'w')

target = 'class'

#%%

for i in range(len(fields)):
    fname, fmap = fields[i]
    if fname == target:
        for obj, ex in (examples):
            if ex[fname] == 'poisonous':
                write_fact(posfile, 'poisonous("%s").', obj)
            else:
                write_fact(negfile, 'poisonous("%s").', obj)
    else:
        for obj, ex in (examples):
            if ex[fname] == '?':
                continue
            write_fact(facts, '%s("%s", "%s").', (fname, obj, ex[fname]))

#%%
facts.close()

posfile.close()
negfile.close()





