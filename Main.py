# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 17:12:16 2018

@author: Will Burke
"""

import numpy as np
import matplotlib.pyplot as plt
from dimension import Dimension
from stackup import Stackup

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------           
# BASIC PROGRAM FLOW FOR ANY TOLSTACK SIMULATION
    # create all dimension objects by invoking instances of Dimension class
        
    # build all stacks you want to analyze
        # stack1 = stackup(dim1,dim2,...)
        
    # build assembly for each stack
        # assembly1 = assemble(stack1)
        
    # check each assembly against upper and lower bounds
        # a1check = assemblycheck(assembly1, lower, upper)
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
       
a = Dimension("housing", 1.5, .1)
b = Dimension("gasket", 1, .01, 4)
c = Dimension("bulkhead", 2, .045, 2)

assy = Stackup("assem1", (a,b,c))

# sample all dimensions
assy.set_samples()

# build stack
print("target value of stackup is: ", assy.get_nominal())
correct,under,over = assy.check(4.45, 4.6)

bi = np.linspace(4,5,100) # standardize binspace for assembly vals only
fig,ax = plt.subplots()
ax.hist(a.get_sample(), alpha=0.5, bins=100)
ax.hist(b.get_sample(), alpha=0.5, bins=100)
ax.hist(c.get_sample(), alpha=0.5, bins=100)
ax.hist(assy.get_stackup_sample(), alpha=0.5, bins=bi)
ax.hist(under,alpha=0.5, color='r', bins=bi)
ax.hist(over, alpha=0.5, color = 'r', bins = bi)
plt.show()
