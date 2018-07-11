# -*- coding: utf-8 -*-
import xlwings as xw
import numpy as np
import matplotlib.pyplot as plt

class Plot:
    def __init__(self):
        # Initialize work sheet objects
        self.sht = xw.Book.caller().sheets[0] # main input sheet
        self.sht2 = xw.Book.caller().sheets[1] # dimension samples sheet
        # Initialize input range objects
        self.dim_range = self.sht.range('D3:I3').options(ndim=2, expand='down')
        self.stack_range = self.sht.range('J3:Q3').options(ndim=2, expand='down')
        self.product_range = self.sht.range('R3:T3').options(ndim=2, expand='down')
        # Initialize plot parameter range objects
        self.plot_bins = self.sht.range('B9')
        self.bin_size = self.plot_bins.value
        if not isinstance(self.bin_size, float) or self.bin_size == 0:
            self.error_rng.value = "Bin size cannot be zero. Check cell B9"
            quit()
        else:
            self.bin_size = int(self.bin_size)
        self.plot_dims = self.sht.range('B11')
        self.plot_stacks = self.sht.range('B16')
        # Initialize error message range
        self.error_rng = self.sht.range('A1')
        self.error_rng.value = "Running..."

    def read(self):

        # Get desired dimension samples
        self.dim_indexes = str(self.plot_dims.value).split(',')
        self.stack_indexes = str(self.plot_stacks.value).split(',')

        self.dim_plot_names=[]
        self.dim_plot_data = []
        if len(self.dim_indexes) > 0 and self.dim_indexes[0] != "None":
            for index in self.dim_indexes:
                i = round(float(index)+1)
                self.dim_plot_data.append(self.sht2.range((2,i)).expand('down').value)
                self.dim_plot_names.append(self.sht2.range((1,i)).value)
                if self.dim_plot_names[-1] == None:
                    self.error_rng.value = "Missing sample for dimension %d" % (i-1)
                    quit()

        # Generate desired stack samples by summing dimension samples
        self.stack_plot_names=[]
        self.stack_plot_data=[]
        self.stack_plot_mask=[] # Data used to mark undersized and oversized samples
        if len(self.dim_indexes) > 0 and self.stack_indexes[0] != "None":
            print(self.stack_indexes)
            for index in self.stack_indexes:
                i = round(float(index))
                if i > len(self.stack_range.value) or self.stack_range.value[i][1] == None:
                    self.error_rng.value = "Invalid stackup index %d in cell B11" % (i)
                    quit()
                dim_inds = self.stack_range.value[i][1].split(',')
                lower = self.stack_range.value[i][2]
                upper = self.stack_range.value[i][3]
                dim_samples = []
                for ind in dim_inds:
                    j = round(float(ind) + 1)
                    if self.sht2.range((1,j)).value == None:
                        self.error_rng.value = "Missing sample for dimension %d" % (i-1)
                        quit()
                    dim_samples.append(self.sht2.range((2,j)).expand('down').value)
                data = [sum(x) for x in zip(*dim_samples)]
                self.stack_plot_data.append(data)
                self.stack_plot_mask.append([i for i in data if i <= lower or i >= upper])
                self.stack_plot_names.append(self.stack_range.value[i][0])

    def draw(self):
        self.read()
        plotted = False
        if self.dim_indexes != None:
            plotted = True
            # Plot dimensions in one figure
            if self.sht.api.Shapes("buttond0").OLEFormat.Object.Value > 0:
                f = plt.figure(0)
                for i in range(0, len(self.dim_plot_data)):
                    plt.gca().hist(self.dim_plot_data[i], alpha=0.5, bins=self.bin_size,
                                   label=self.dim_plot_names[i])
                plt.legend()
            # Plot dimensions in one figure, multiple plots
            elif self.sht.api.Shapes("buttond1").OLEFormat.Object.Value > 0:
                f, axs = plt.subplots(len(self.dim_plot_data), 1, sharey=True)
                for i in range(0, len(self.dim_plot_data), 1):
                    axs[i].hist(self.dim_plot_data[i], alpha=0.5, bins=self.bin_size,
                                label=self.dim_plot_names[i], facecolor='b')
                    axs[i].legend()
            # Plot dimensions in multiple figures
            else:
                for i in range(0, len(self.dim_plot_data)):
                    f = plt.figure(i)
                    plt.title(self.dim_plot_names[i])
                    plt.gca().hist(self.dim_plot_data[i], alpha=0.5, bins=self.bin_size, facecolor='b')
        if self.stack_indexes != None:
            plotted = True
            # Plot stackups in one figure
            if self.sht.api.Shapes("buttons0").OLEFormat.Object.Value > 0:
                f = plt.figure(len(self.stack_plot_data))
                for i in range(0, len(self.stack_plot_data)):
                    plt.gca().hist(self.stack_plot_data[i], alpha=0.5, bins=self.bin_size,
                                   label=self.stack_plot_names[i])
                    plt.gca().hist(self.stack_plot_mask[i], alpha=1, bins=self.bin_size, facecolor='r')
                plt.legend()
            # Plot stackups in one figure, multiple plots
            elif self.sht.api.Shapes("buttons1").OLEFormat.Object.Value > 0:
                f, axs = plt.subplots(len(self.stack_plot_data), 1)
                for i in range(0, len(self.stack_plot_data), 1):
                    axs[i].hist(self.stack_plot_data[i], alpha=0.5, bins=self.bin_size,
                                label=self.stack_plot_names[i], facecolor='g')
                    axs[i].hist(self.stack_plot_mask[i], alpha=1, bins=self.bin_size, facecolor='r')
                    axs[i].legend()
            # Plot stackups in multiple figures
            else:
                for i in range(0, len(self.stack_plot_data)):
                    f = plt.figure(i+len(self.dim_plot_data))
                    plt.title(self.stack_plot_names[i])
                    plt.gca().hist(self.stack_plot_data[i], alpha=0.5, bins=self.bin_size, facecolor='g')
                    plt.gca().hist(self.stack_plot_mask[i], alpha=1, bins=self.bin_size, facecolor='r')
        if plotted == True:
            self.error_rng.value = "Waiting for figures to close..."
            plt.show()
        self.error_rng.value = "Ready"
                
if __name__ == "__main__":
    # Used when running from Python
    xw.Book('Dimension.xlsm').set_mock_caller()
    # Used for frozen executable
    plot = Plot()
    plot.draw()
