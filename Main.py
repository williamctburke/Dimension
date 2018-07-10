# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 17:12:16 2018

@author: Will Burke
"""

import numpy as np
import matplotlib.pyplot as plt
from dimension import Dimension
from stackup import Stackup
from part import Part

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------           
# BASIC PROGRAM FLOW FOR ANY TOLSTACK SIMULATION
    # create all dimension objects by invoking instances of Dimension class
        # dim1 = Dimension("housing", dim, tol, stddev)
    # build all stacks you want to analyze
        # stack1 = Stackup("assem", (dim1,dim2,...))
        
    # get samples from random distribution for a given stackup
        # stack1.set_samples()
    # alternatively get samples for every dimension created
        # 
        
    # check each assembly against upper and lower bounds
        # results = stack1.test(lower, upper)
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
       
a = Dimension("housing", 1.5, .1)
b = Dimension("gasket", 1, .01, 4)
c = Dimension("bulkhead", 2, .045, 2)
d = Dimension("pin", 0.5, 0.005, 4)

stack = Stackup("stack1", (a,b,c), 4.45, 4.6)
stack2 = Stackup("stack2", (a,d), 1.9, 2.1)

part = Part("part", (stack, stack2))

# sample all dimensions
Dimension.set_all_samples()

# build stack
print("target value of stackup is: ", stack.get_nominal())
_,correct,under,over = stack.test()

n = len(correct) + len(under) + len(over)
print("Pass %: ",(len(correct)/n))
print("Undersized %: ",(len(under)/n))
print("Oversized %: ",(len(over)/n))

results = part.test()
print("Part success rate: %: ", (sum(results)/len(results)))

bi = np.linspace(4,5,100) # standardize binspace for assembly vals only
fig,ax = plt.subplots()
ax.hist(a.get_sample(), alpha=0.5, bins=100)
ax.hist(b.get_sample(), alpha=0.5, bins=100)
ax.hist(c.get_sample(), alpha=0.5, bins=100)
ax.hist(d.get_sample(), alpha=0.5, bins=100)
ax.hist(stack.get_stackup_sample(), alpha=0.5, bins=bi)
ax.hist(under,alpha=0.5, color='r', bins=bi)
ax.hist(over, alpha=0.5, color = 'r', bins = bi)
plt.show()
