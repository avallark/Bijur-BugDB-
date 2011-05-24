#!/usr/bin/env python

import pickle




f = open('people.csv','r')

a = f.readlines()

final = []

for i in a[0].split('\r'):
    entry = i.split(';')
    final.append(entry)

findict = {}

for i in range(1,len(final)):
    findict[i] = final[i-1]
    
f.close()

f = open('pickled.ab','w')

pickle.dump(findict, f)

f.close()


