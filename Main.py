# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 17:12:16 2018

@author: Will Burke
"""
import xlwings as xw
from dimension import Dimension
from stackup import Stackup
from product import Product

class Main:
    sample_count = 100000
    def __init__(self):
        # Initialize work sheet objects
        self.sht = xw.Book.caller().sheets[0] # main input sheet
        self.sht2 = xw.Book.caller().sheets[1] # dimension samples sheet
        self.sht3 = xw.Book.caller().sheets[2] # part samples sheet
        # Initialize input range objects
        self.dim_range = self.sht.range('C3:H3').options(ndim=2, expand='down')
        self.stack_range = self.sht.range('I3:P3').options(ndim=2, expand='down')
        self.product_range = self.sht.range('Q3:S3').options(ndim=2, expand='down')
    def simulate(self):
        self.read()
        for dim in self.dimensions:
            dim.set_sample(int(self.sht.range('B3').value))
        self.update()
    def read(self):
        # Generate dimension, stackup, and product objects from user input
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
            self.sht.range('M'+str(i+3)).value = self.stackups[i].get_nominal()
        self.products = []
        for row in self.product_range.value:
            stacks = []
            for index in row[1].split(','):
                stacks.append(self.stackups[int(index)-3])
            self.products.append(Product(row[0], stacks))
    def update(self):
        # Fill output cells
        for i in range(0, len(self.stackups)):
            row = str(i+3)
            _,correct,under,over = self.stackups[i].test()
            n = len(correct) + len(under) + len(over)
            self.sht.range('N'+row).value = (len(correct)/n)
            self.sht.range('O'+row).value = (len(under)/n)
            self.sht.range('P'+row).value = (len(over)/n)   
        for i in range(0, len(self.products)):
            row = str(i+3)
            results = self.products[0].test()
            self.sht.range('S'+row).value = (sum(results)/len(results))
        if self.sht.range('B4').value != None and self.sht.range('B4').value != 0:
            self.write_dims()
        if self.sht.range('B5').value != None and self.sht.range('B5').value != 0:
            self.write_stacks()
    def write_dims(self):
        index = 1
        for dim in self.dimensions:
            self.sht2.range((1,index)).value = dim.name
            self.sht2.range((2,index)).options(transpose=True).value = dim.get_sample()
            index += 1
    def write_stacks(self):
        index = 1
        for stack in self.stackups:
            self.sht3.range((1,index)).value = stack.name
            self.sht3.range((2,index)).options(transpose=True).value = stack.get_stackup_sample()
            index += 1
if __name__ == "__main__":
    # Used when running from Python
    xw.Book('Dimension.xlsm').set_mock_caller()
    # Used for frozen executable
    main = Main()
    main.simulate()
