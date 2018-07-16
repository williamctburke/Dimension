# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 17:12:16 2018

@author: Will Burke
"""
import xlwings as xw
from dimension import Dimension
from stackup import Stackup
from product import Product
import sys

import scipy.stats as st

DISTRIBUTIONS = [        
    st.alpha,st.anglit,st.arcsine,st.beta,st.betaprime,st.bradford,st.burr,st.cauchy,st.chi,st.chi2,st.cosine,
    st.dgamma,st.dweibull,st.erlang,st.expon,st.exponnorm,st.exponweib,st.exponpow,st.f,st.fatiguelife,st.fisk,
    st.foldcauchy,st.foldnorm,st.frechet_r,st.frechet_l,st.genlogistic,st.genpareto,st.gennorm,st.genexpon,
    st.genextreme,st.gausshyper,st.gamma,st.gengamma,st.genhalflogistic,st.gilbrat,st.gompertz,st.gumbel_r,
    st.gumbel_l,st.halfcauchy,st.halflogistic,st.halfnorm,st.halfgennorm,st.hypsecant,st.invgamma,st.invgauss,
    st.invweibull,st.johnsonsb,st.johnsonsu,st.ksone,st.kstwobign,st.laplace,st.levy,st.levy_l,st.levy_stable,
    st.logistic,st.loggamma,st.loglaplace,st.lognorm,st.lomax,st.maxwell,st.mielke,st.nakagami,st.ncx2,st.ncf,
    st.nct,st.norm,st.pareto,st.pearson3,st.powerlaw,st.powerlognorm,st.powernorm,st.rdist,st.reciprocal,
    st.rayleigh,st.rice,st.recipinvgauss,st.semicircular,st.t,st.triang,st.truncexpon,st.truncnorm,st.tukeylambda,
    st.uniform,st.vonmises,st.vonmises_line,st.wald,st.weibull_min,st.weibull_max,st.wrapcauchy
    ]

class Main:
    sample_count = 100000 #dynamically modified by reading cell B5
    def __init__(self):
        # Initialize work sheet objects
        self.sht = xw.Book.caller().sheets[0] # main input sheet
        self.sht2 = xw.Book.caller().sheets[1] # dimension samples sheet, populated with samples generated by numpy
        self.sht3 = xw.Book.caller().sheets[2] # dimension actual measurements sheet, populated by the user for fitting distributions
        # Initialize input range objects
        self.dim_range = self.sht.range('D3:I3').options(ndim=2, expand='down') # expand allows the range to dynamically include any number of rows
        self.stack_range = self.sht.range('J3:Q3').options(ndim=2, expand='down')
        self.product_range = self.sht.range('R3:T3').options(ndim=2, expand='down')
        self.sht.range('N3:Q4').expand('down').clear_contents() # clean up any old output from previous uses of the tool
        self.sht.range('T3').expand('down').clear_contents()
        # Initialize output range
        self.dim_start_col = 'D'
        self.stack_start_col = 'J'
        self.prod_start_col = 'R'
        self.stack_nominal_col = 'N'
        self.stack_pass_col = 'O'
        self.stack_under_col = 'P'
        self.stack_over_col = 'Q'
        self.prod_pass_col = 'T'
        self.sample_output_cell = 'A1'
        # Initialize error message range
        self.error_rng = self.sht.range('A1')
        self.error_rng.value = "Running..."
        # Initialize sample parameter range
        Main.sample_count = int(self.sht.range('B5').value)

        if Main.sample_count == 0:
            self.error_rng.value = "Sample count cannot be zero. Check cell B5"
            sys.exit()
        
    def simulate(self):
        self.read() # The settings for each dim are populated in the read() method
        n = Main.sample_count
        for dim in self.dimensions:
            s = dim.dist_func.rvs(*dim.params, size = n)
            dim.set_sample(s) 

        self.update()
        self.error_rng.value = "Ready"
        
    def read(self):
        # Generate dimension, stackup, and product objects from user input
        self.dimensions = []
        for i in range(0, len(self.dim_range.value)):
            self.check_dim(i)
            row = self.dim_range.value[i]
            self.dimensions.append(Dimension(row[0], row[1], row[2], row[3], row[4], row[5]))
            dim = self.dimensions[-1]
            if dim.dist == "normal":
                best_dist = st.norm
                best_params = (dim.dim, dim.stddev)
            else:
                params = self.sht3.range((2,i+2)).value
                if params == None:
                    self.error_rng.value = "Missing parameters for dimension %d, fit data first" % (i)
                    sys.exit()
                else:
                    params = params.split(',')
                best_params = [float(i) for i in params[1:]]
                best_dist = DISTRIBUTIONS[int(round(float(params[0])))]
            self.dimensions[-1].set_dist(best_dist, best_params)
        self.stackups = []
        for i in range(0, len(self.stack_range.value)):
            self.check_stack(i)
            row = self.stack_range.value[i]
            dims = []
            for index in str(row[1]).split(','): # parse dimension references in column K
                dims.append(self.dimensions[round(float(index))])
            self.stackups.append(Stackup(row[0], dims, row[2], row[3]))
            self.sht.range(self.stack_nominal_col+str(i+3)).value = self.stackups[i].get_nominal()
        self.products = []
        for i in range(0, len(self.product_range.value)):
            self.check_prod(i)
            row = self.product_range.value[i]
            stacks = []
            for index in str(row[1]).split(','): # parse stackup references in column S
                stacks.append(self.stackups[round(float(index))])
            self.products.append(Product(row[0], stacks))

    def get_distribution():
        pass
            
    def update(self):
        # Fill output cells
        for i in range(0, len(self.stackups)):
            row = str(i+3)
            _,correct,under,over = self.stackups[i].test()
            n = len(correct) + len(under) + len(over)
            self.sht.range(self.stack_pass_col+row).value = (len(correct)/n)
            self.sht.range(self.stack_under_col+row).value = (len(under)/n)
            self.sht.range(self.stack_over_col+row).value = (len(over)/n)   
        for i in range(0, len(self.products)):
            row = str(i+3)
            results = self.products[0].test()
            self.sht.range(self.prod_pass_col+row).value = (sum(results)/len(results))
        # Read from check box
        if self.sht.api.Shapes("check0").OLEFormat.Object.Value > 0:
            self.write_samples()
            
    def write_samples(self):
        index = 1
        self.sht2.range(self.sample_output_cell).expand().clear()
        for dim in self.dimensions:
            self.sht2.range((1,index)).value = dim.name
            self.sht2.range((2,index)).options(transpose=True).value = dim.get_sample()
            index += 1
            
    def check_dim(self, dim_ind):
        dim = self.dim_range.value[dim_ind]
        for i in range(0,3):
            if dim[i] == None:
                self.error_rng.value = "Missing required field in dimension %d, cell %s%d" % (dim_ind, chr(ord(self.dim_start_col)+i), dim_ind+3)
                sys.exit()
                
    def check_stack(self, stack_ind):
        stack = self.stack_range.value[stack_ind]
        for i in range(0,4):
            if stack[i] == None:
                self.error_rng.value = "Missing required field in stackup %d, cell %s%d" % (stack_ind, chr(ord(self.stack_start_col)+i), stack_ind+3)
                sys.exit()
        for ind in str(stack[1]).split(','):
            i = round(float(ind))
            if i > len(self.dim_range.value)-1 or self.dim_range.value[i] == None:
                self.error_rng.value = "Invalid reference to dimension %d in cell %s%d" % (i, chr(ord(self.stack_start_col)+1), stack_ind+3)
                sys.exit()
                
    def check_prod(self, prod_ind):
        prod = self.product_range.value[prod_ind]
        for i in range(0,2):
            if prod[i] == None:
                self.error_rng.value = "Missing required field in product %d, cell %s%d" % (prod_ind, chr(ord(self.prod_start_col)+i), prod_ind+3)
                sys.exit()
        for ind in str(prod[1]).split(','):
            i = round(float(ind))
            if i > len(self.stack_range.value)-1 or self.stack_range.value[i] == None:
                self.error_rng.value = "Invalid reference to stackup %d in cell %s%d" % (i,chr(ord(self.prod_start_col)+1), prod_ind+3)
                sys.exit()

if __name__ == "__main__":
    # Used to set the Excel file in stand-alone mode
    xw.Book('Dimension_standalone.xlsm').set_mock_caller()
    # Used for frozen executable
    main = Main()
    main.simulate()