# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 17:12:16 2018

@author: Will Burke
"""
import xlwings as xw
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
class Main:
    sample_count = 100000
    def __init__(self):
        #sht = xw.Book.caller().sheets[0]
        self.sht = xw.Book('Dimension.xlsm').sheets[0]
        self.sht2 = xw.Book('Dimension.xlsm').sheets[1]
        self.dim_range = self.sht.range('A3:F3').options(ndim=2, expand='down')
        self.stack_range = self.sht.range('G3:J3').options(ndim=2, expand='down')
        self.part_range = self.sht.range('O3:P3').options(ndim=2, expand='down')
    def simulate(self):
        for dim in self.dimensions:
            dim.set_sample(int(self.sht.range('S1').value))
        self.update()
    def read(self):
        self.dimensions = []
        for row in self.dim_range.value:
            self.dimensions.append(Dimension(row[0], row[1], row[2], row[3], row[4], row[5]))
        self.stackups = []
        for i in range(0, len(self.stack_range.value)):
            row = self.stack_range.value[i]
            dims = []
            for index in row[1].split(','):
                dims.append(self.dimensions[int(index)-3])
            self.stackups.append(Stackup(row[0], dims, row[2], row[3]))
            self.sht.range('K'+str(i+3)).value = self.stackups[i].get_nominal()
        self.parts = []
        for row in self.part_range.value:
            stacks = []
            for index in row[1].split(','):
                stacks.append(self.stackups[int(index)-3])
            self.parts.append(Part(row[0], stacks))
    def update(self):
        for i in range(0, len(self.stackups)):
            row = str(i+3)
            _,correct,under,over = self.stackups[i].test()
            n = len(correct) + len(under) + len(over)
            self.sht.range('L'+row).value = (len(correct)/n)
            self.sht.range('M'+row).value = (len(under)/n)
            self.sht.range('N'+row).value = (len(over)/n)

        for i in range(0, len(self.parts)):
            row = str(i+3)
            results = self.parts[0].test()
            self.sht.range('Q'+row).value = (sum(results)/len(results))
            
        bi = np.linspace(4,5,100) # standardize binspace for assembly vals only
        fig,ax = plt.subplots()
        for dim in self.dimensions:
            ax.hist(dim.get_sample(), alpha=0.5, bins=100)
        ax.hist(self.stackups[0].get_stackup_sample(), alpha=0.5, bins=bi)
        ax.hist(under,alpha=0.5, color='r', bins=bi)
        ax.hist(over, alpha=0.5, color = 'r', bins = bi)
        self.sht.pictures.add(fig, name="Analysis", update=True)

if __name__ == "__main__":
    # Used for frozen executable
    main = Main()
    main.read()
    main.simulate()
