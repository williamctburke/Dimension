# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 17:12:16 2018

@author: Will Burke
"""

import numpy as np
import matplotlib.pyplot as plt
from Classes import Dim


def dimsample(*dimensions):
    """
    input: an arbitrary number of Dimension objects
    output: sets sample and shifted for each Dim object
    """
    for d in dimensions:
        d.set_sample()
        d.set_shifted()
        
def stackup(*dimensions):
    """
    input: an arbitrary number of Dimension objects
    out: returns a list of Dimension objects associated with 
    a physical tolerance stack
    """
    stack = []
    for d in dimensions:
        stack.append(d)
    return stack

def nominal(stack):
    """
    input: a list of Dimension objects, eg: a stack
    out: the nominal or target as designed value for the stack
    """
    nom = 0
    for dim in stack:
        nom += dim.dim
    return nom

def assemble(stack):
    """
    input: a list of Dimension objects, eg: a stack
    out: a list of as assembled dimensions, with one dimensions
    for each simulated assembly of the stack
    """
    metasample = []
    for dim in stack:
        metasample.append(dim.get_sample())
    assembly = [sum(x) for x in zip(*metasample)] #super cool! zip an arbitrary length of lists!
    return assembly

def assemblycheck(assembly,lower,upper):
    """
    input: an "assembly", or <list> of as assembled dimensions from each 
    Dimension of a sampled stack
    out: % pass rate, % oversized, % undersized <floats>
    """
    n = len(assembly)
    over = []
    under = []
    correct = []
    for i in assembly:
        if i < lower:
            under.append(i)
        elif i > upper:
            over.append(i)
        else:
            correct.append(i)
    print("Pass %: ",(len(correct)/n))
    print("Undersized %: ",(len(under)/n))
    print("Oversized %: ",(len(over)/n))
    return (correct, under, over)
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------           
# BASIC PROGRAM FLOW FOR ANY TOLSTACK SIMULATION
    # create all dimension objects by invoking instances of Dimension class
    
    # sample all dimsion objects with dimsample()
    
    # build all stacks you want to analyze
        # stack1 = stackup(dim1,dim2,...)
        
    # build assembly for each stack
        # assembly1 = assemble(stack1)
        
    # check each assembly against upper and lower bounds
        # a1check = assemblycheck(assembly1, lower, upper)
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
       
a = Dim("housing", 1.5, .1)
b = Dim("gasket", 1, .01, 4)
c = Dim("bulkhead", 2, .045, 2)

# sample all dimensions
dimsample(a,b,c)

# build stack
stack = stackup(a,b,c)
assembly = assemble(stack)
nom = nominal(stack)
print("target value of stackup is: ", nom)
correct,under,over = assemblycheck(assembly, 4.45, 4.6)

bi = np.linspace(4,5,100) # standardize binspace for assembly vals only
fig,ax = plt.subplots()
ax.hist(a.get_sample(), alpha=0.5, bins=100)
ax.hist(b.get_sample(), alpha=0.5, bins=100)
ax.hist(c.get_sample(), alpha=0.5, bins=100)
ax.hist(assembly, alpha=0.5, bins=bi)
ax.hist(under,alpha=0.5, color='r', bins=bi)
ax.hist(over, alpha=0.5, color = 'r', bins = bi)
plt.show()
