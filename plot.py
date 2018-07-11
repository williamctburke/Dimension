# -*- coding: utf-8 -*-
import xlwings as xw
import numpy as np
import matplotlib.pyplot as plt

class Plot:
    sample_count = 100000
    def __init__(self):
        # Initialize work sheet objects
        self.sht = xw.Book.caller().sheets[0] # main input sheet
        self.sht2 = xw.Book.caller().sheets[1] # dimension samples sheet
        # Initialize input range objects
        self.dim_range = self.sht.range('D3:I3').options(ndim=2, expand='down')
        self.stack_range = self.sht.range('J3:Q3').options(ndim=2, expand='down')
        self.product_range = self.sht.range('R3:T3').options(ndim=2, expand='down')
        # Initialize plot parameter range objects
        self.plot_dims = self.sht.range('B9')
        self.plot_stacks = self.sht.range('B11')
        # Initialize error message range
        self.error_rng = self.sht.range('A16')
        self.error_rng.value = "Running..."

    def read(self):
        # Get desired dimension samples
        self.dim_indexes = str(self.plot_dims.value).split(',')
        self.stack_indexes = str(self.plot_stacks.value).split(',')

        self.dim_plot_names=[]
        self.dim_plot_data = []
        for index in self.dim_indexes:
            i = round(float(index)+1)
            rng = self.sht2.range((2,i)).options(expand='down')
            self.dim_plot_data.append(rng.value)
            self.dim_plot_names.append(self.sht2.range((1,i)).value)
            if self.dim_plot_names[-1] == None:
                self.error_rng.value = "Missing sample for dimension %d" % (i-1)
                quit()
        self.stack_plot_names=[]
        self.stack_plot_data=[]
        for index in self.stack_indexes:
            i = round(float(index))
            if i > len(self.stack_range.value) or self.stack_range.value[i][1] == None:
                self.error_rng.value = "Invalid stackup index %d in cell B11" % (i)
                quit()
            dim_inds = self.stack_range.value[i][1].split(',')
            dim_samples = []
            for ind in dim_inds:
                j = round(float(ind) + 1)
                if self.sht2.range((1,j)).value == None:
                    self.error_rng.value = "Missing sample for dimension %d" % (i-1)
                    quit()
                dim_samples.append(self.sht2.range((2,j)).options(expand='down').value)
            self.stack_plot_data.append([sum(x) for x in zip(*dim_samples)])
            self.stack_plot_names.append(self.stack_range.value[i][0])

    def draw(self):
        self.read()
        fig,ax = plt.subplots()
        for data in self.dim_plot_data:
            ax.hist(data, alpha=0.5, bins=100)
        print(self.sht.api.Shapes("check1").OLEFormat.Object.Value)
        plt.show()

        fig,ax = plt.subplots()
        for data in self.stack_plot_data:
            ax.hist(data, alpha=0.5, bins=100)
        self.error_rng.value = "Done"

    
if __name__ == "__main__":
    # Used when running from Python
    xw.Book('Dimension.xlsm').set_mock_caller()
    # Used for frozen executable
    plot = Plot()
    plot.draw()
