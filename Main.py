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
        # Initialize input range objects
        self.dim_range = self.sht.range('D3:I3').options(ndim=2, expand='down')
        self.stack_range = self.sht.range('J3:Q3').options(ndim=2, expand='down')
        self.product_range = self.sht.range('R3:T3').options(ndim=2, expand='down')
        self.sht.range('N3:Q4').expand('down').clear_contents()
        self.sht.range('T3').expand('down').clear_contents()
        # Initialize error message range
        self.error_rng = self.sht.range('A15')
        self.error_rng.value = "Running..."
        
    def simulate(self):
        self.read()
        Main.sample_count = int(self.sht.range('B3').value)
        for dim in self.dimensions:
            dim.set_sample(Main.sample_count)
        self.update()
        self.error_rng.value = "Done"
        
    def read(self):
        # Generate dimension, stackup, and product objects from user input
        self.dimensions = []
        for i in range(0, len(self.dim_range.value)):
            self.check_dim(i)
            row = self.dim_range.value[i]
            self.dimensions.append(Dimension(row[0], row[1], row[2], row[3], row[4], row[5]))
        self.stackups = []
        for i in range(0, len(self.stack_range.value)):
            self.check_stack(i)
            row = self.stack_range.value[i]
            dims = []
            for index in str(row[1]).split(','):
                dims.append(self.dimensions[round(float(index))])
            self.stackups.append(Stackup(row[0], dims, row[2], row[3]))
            self.sht.range('N'+str(i+3)).value = self.stackups[i].get_nominal()
        self.products = []
        for i in range(0, len(self.product_range.value)):
            self.check_prod(i)
            row = self.product_range.value[i]
            stacks = []
            for index in str(row[1]).split(','):
                stacks.append(self.stackups[round(float(index))])
            self.products.append(Product(row[0], stacks))
            
    def update(self):
        # Fill output cells
        for i in range(0, len(self.stackups)):
            row = str(i+3)
            _,correct,under,over = self.stackups[i].test()
            n = len(correct) + len(under) + len(over)
            self.sht.range('O'+row).value = (len(correct)/n)
            self.sht.range('P'+row).value = (len(under)/n)
            self.sht.range('Q'+row).value = (len(over)/n)   
        for i in range(0, len(self.products)):
            row = str(i+3)
            results = self.products[0].test()
            self.sht.range('T'+row).value = (sum(results)/len(results))
        if self.sht.api.Shapes("check0").OLEFormat.Object.Value == 1:
            self.write_dims()
            
    def write_dims(self):
        index = 1
        self.sht2.range('A1').expand().clear()
        for dim in self.dimensions:
            self.sht2.range((1,index)).value = dim.name
            self.sht2.range((2,index)).options(transpose=True).value = dim.get_sample()
            index += 1
            
    def check_dim(self, dim_ind):
        dim = self.dim_range.value[dim_ind]
        for i in range(0,3):
            if dim[i] == None:
                self.error_rng.value = "Missing required field in dimension %d, cell %s%d" % (dim_ind, chr(ord('D')+i), dim_ind+3)
                quit()
                
    def check_stack(self, stack_ind):
        stack = self.stack_range.value[stack_ind]
        for i in range(0,4):
            if stack[i] == None:
                self.error_rng.value = "Missing required field in stackup %d, cell %s%d" % (stack_ind, chr(ord('J')+i), stack_ind+3)
                quit()
        for ind in str(stack[1]).split(','):
            i = round(float(ind))
            if i > len(self.dim_range.value)-1 or self.dim_range.value[i] == None:
                self.error_rng.value = "Invalid reference to dimension %d in cell K%d" % (i, stack_ind+3)
                quit()
                
    def check_prod(self, prod_ind):
        prod = self.product_range.value[prod_ind]
        for i in range(0,2):
            if prod[i] == None:
                self.error_rng.value = "Missing required field in product %d, cell %s%d" % (prod_ind, chr(ord('R')+i), prod_ind+3)
                quit()
        for ind in str(prod[1]).split(','):
            i = round(float(ind))
            if i > len(self.stack_range.value)-1 or self.stack_range.value[i] == None:
                self.error_rng.value = "Invalid reference to stackup %d in cell S%d" % (i, prod_ind+3)
                quit()
                
if __name__ == "__main__":
    # Used when running from Python
    xw.Book('Dimension.xlsm').set_mock_caller()
    # Used for frozen executable
    main = Main()
    main.simulate()
