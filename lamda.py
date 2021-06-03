#!/usr/bin/env python
# coding: utf-8

# In[17]:


import math
import os

nrep = 9
tmin = 300
tmax = 1000

temps = []

for i in range (0,nrep):
    temp = tmin*math.exp(i*math.log(tmax/tmin)/(nrep-1))
    temps.append(temp)
print(temps)

lambds = []
for i in temps:
    lambd = (i/tmax)
    lambds.append(lambd)

lambds.reverse()
print(lambds)

for i in range(0,nrep):

    # os.system("mkdir R$i;cp aladi_si.gro R$i;cp nvt* R$i;cp em* R$i; cp md* R$i;cp processed.top R$i;cp plumed.dat R$i ;cd R$i")
    lam = lambds[i]
    print(lam)
    os.chdir("R"+str(i))
    os.system("pwd")
    os.system("plumed partial_tempering "+str(lam)+" < processed.top > topol"+str(i)+".top")
    os.chdir("..")
print("done")
