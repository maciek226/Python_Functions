import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import pandas as pd
import numpy as np

import os
"""
This is a convenience class that allows for making nice plots, easily 
"""

class PlotData:
    debug = bool
    file_path = str()
    title = str()

    save_directory = str()

    save_fig = bool()

    line_plot_margin = 1

    columns = int()
    rows = int()

    available_data = dict()
    data_list = list()
    fig = plt.figure
    axes = list()

### Plot Setup 
    def __init__(self, path, debug = False):
        self.file_path = path
        self.debug = debug

        self.fig = plt.figure()
        self.data = pd.read_csv(self.file_path)

        # Read the header data
        headers = self.data.head()
        cc = 0
        self.debug_print("\nThis is the data in the provided file:")
        for item in headers:
            self.debug_print("\t%s"%(item))
            self.available_data[item]=(cc)
            self.data_list.append( np.array(self.data.loc[:,item]) )
            cc += 1
    
    def set_fig_size(self,width,height):
        self.fig.set_size_inches(width,height)

    # Allows for manual control of the plot positioning 
    def plot_setup(self, rows, columns, title = "Plot Title"):
        self.columns = columns
        self.rows = rows
        
        # Puts in a temp title 
        self.fig.suptitle(title, fontsize=16)
        
        # If only one thing is plotted, it creates and appends that plot 
        if columns == 1 and rows == 1:
            plt.plot()
            self.axes.append(plt.gca())
        # If many plots are being added, they are created in the while loop
        # with place holder titles
        else:
            ee = 1
            for cc in range(0,rows):
                for dd in range(0,columns):
                    self.axes.append(plt.subplot(rows,columns,ee))
                    self.axes[ee-1].set_title(ee-1)
                    ee += 1
    
    # sets shared axes for two plots 
    # TODO: vectorized this 
    def share_x_axis(self, index1, index2):
        self.axes[index1].get_shared_x_axes().join(self.axes[index1],self.axes[index2])
    
    def share_y_axis(self, index1, index2):
        self.axes[index1].get_shared_y_axes().join(self.axes[index1],self.axes[index2])
    
### axis labels and ticks
    def set_y_axis_title(self,index,title):
        if isinstance(index,list):
            for cc in index:
                self.axes[cc].set_ylabel(title)
        else:
            self.axes[index].set_ylabel(title)

    def set_x_axis_title(self,index,title):
        if isinstance(index,list):
            for cc in index:
                self.axes[cc].set_xlabel(title)
        else:
            self.axes[index].set_xlabel(title)

    # This is a hack that changes the scale of the y-Axis 
    # this can be done for x-Axis too, but 
    def set_y_axis_scale_mili(self, index):
        def mili(x, pos):
            return "%1.1f"%(x*10**3)
        format = FuncFormatter(mili)
        if isinstance(index,list):
            for cc in index:
                self.axes[cc].yaxis.set_major_formatter(format)
        else:
            self.axes[index].yaxis.set_major_formatter(format)

    def hide_x_ticks(self,index):
        if isinstance(index,list):
            for cc in index:
                self.axes[cc].xaxis.set_visible(False)
        else:
                self.axes[index].xaxis.set_visible(False)
        
    def set_vertical_x_label(self, index):
        if isinstance(index,list):
            for cc in index:
                plt.sca(self.axes[cc])
                plt.xticks(rotation=90)
        else:
                plt.sca(self.axes[index])
                plt.xticks(rotation=90)

    def set_x_label_range(self,index,min,step,max):
        plt.sca(self.axes[index])
        plt.xticks(np.arange(min,max,step=step))

    # Autofit data functions look at the data, and set the min and max values
    # 10% more/less than the data limits 
    # TODO: Create an alternative mode based on stats 
    def auto_fit_y_data(self,index,data_name):
        y_index = self.available_data[data_name]
        min_value = np.min(self.data_list[y_index])
        max_value = np.max(self.data_list[y_index])

        if min_value < 0:
            min_value *= 1.1
        else:
            min_value *= 0.9
        
        if max_value < 0:
            max_value *= 0.9
        else:
            max_value *= 1.1
        
        if min_value == max_value:
            min_value = 0
            max_value = 1 
        self.set_ylimit(index, min_value, max_value)

    def auto_fit_x_data(self,index,data_name):
        x_index = self.available_data[data_name]
        min_value = np.min(self.data_list[x_index])
        max_value = np.max(self.data_list[x_index])
        self.set_xlimit(index, min_value, max_value)
        #self.axes[index].set_xlim([min_value, max_value])

    # TODO: Advanced Autofit

    def set_xlimit(self, index, lower, upper):
        self.axes[index].set_xlim([lower, upper])

    def set_ylimit(self, index, lower, upper):
        self.axes[index].set_ylim([lower, upper])

    def split_line(self, x_name, y_name):
        # Load x and y data and find the lenght of either one 
        x_index = self.available_data[x_name]
        y_index = self.available_data[y_name]
        data_len = self.data_list[x_index].size


        # Find location of min value 
        x_min = np.argmin(self.data_list[x_index])
        self.debug_print("Data Length is %i and the min value is located at %i"%(data_len,x_min))
        # because there are multiple readings at each step and there may be some movment 
        # the min x value may not correspond to the actual min value 
        for cc in range(1,data_len):
            if abs(self.data_list[x_index][cc-1] - self.data_list[x_index][cc]) > 10:
                self.debug_print("Gap found between %i with %1.11f and %i with %1.11f"%(cc-1,self.data_list[x_index][cc-1], cc, self.data_list[x_index][cc]))
                x_min = cc
                break
        
        # Create a new empty arrays that will be 
        x_data_rearranged = np.empty([*self.data_list[x_index].shape])
        y_data_rearranged = np.empty([*self.data_list[y_index].shape])

        # Put the starting data at the start of the array 
        # For simplicity these these the data is divided and recobined

        fist_x_chunk = self.data_list[x_index][x_min:]
        second_x_chunk = self.data_list[x_index][:x_min]

        first_y_chunk = self.data_list[y_index][x_min:]
        second_y_chunk = self.data_list[y_index][:x_min]

        x_data_rearranged[:fist_x_chunk.size] = fist_x_chunk
        x_data_rearranged[fist_x_chunk.size:] = second_x_chunk
        
        y_data_rearranged[:fist_x_chunk.size] = first_y_chunk
        y_data_rearranged[fist_x_chunk.size:] = second_y_chunk

        return x_data_rearranged, y_data_rearranged
        # self.plot_data_direct(index, x_data_rearranged, y_data_rearranged)
        
    # Plots the data to the selected plot 
    # for not it only supports scatter plots 
    def plot_data(self, index, x_name, y_name, plot_type = 'scatter', color = "", title = ""):
        x_index = self.available_data[x_name]
        y_index = self.available_data[y_name]
        #print(type(self.axes))
        if plot_type == 'scatter':
            self.axes[index].scatter(self.data_list[x_index],self.data_list[y_index],s=.5,color='tab:'+color)
            self.auto_fit_y_data(index, y_name)
            self.auto_fit_x_data(index, x_name)
        if plot_type == 'line':
            x_new, y_new = self.split_line(x_name, y_name)
            self.axes[index].plot(x_new[self.line_plot_margin:-self.line_plot_margin],y_new[self.line_plot_margin:-self.line_plot_margin],color='tab:'+color)
            self.auto_fit_y_data(index, y_name)
            self.auto_fit_x_data(index, x_name)
        else:
            Exception("Feature not yet avalabile... or you made a typo")
        if not title == "":
            self.axes[index].set_title(title)
    
    def plot_data_direct(self, index, x_data, y_data, plot_type = 'scatter', color = "", title = ""):
        if plot_type == 'scatter':
            plt.sca(self.axes[index])
            self.axes[index].scatter(x_data,y_data,s=.75,color='tab:'+color)
            # self.auto_fit_y_data(index, y_name)
            # self.auto_fit_x_data(index, x_name)
        # if plot_type == 'line':
        #     x_new, y_new = self.split_line(x_name, y_name)
        #     self.axes[index].plot(x_new[self.line_plot_margin:-self.line_plot_margin],y_new[self.line_plot_margin:-self.line_plot_margin],color='tab:'+color)
            # self.auto_fit_y_data(index, y_name)
            # self.auto_fit_x_data(index, x_name)
        else:
            Exception("Feature not yet avalabile... or you made a typo")
        if not title == "":
            self.axes[index].set_title(title)
### Saving 
    def save_figure(self):
        self.save_directory = os.path.dirname(self.file_path)
        file_name = self.generate_file_name()
        self.fig.savefig(file_name)
    
    # Generates file name for the plot
    def generate_file_name(self):
        # Get the neame of the file 
        data_file_name = os.path.basename(self.file_path)
        
        # If the file does not exist, just change the extension 
        if not os.path.isfile(self.file_path[:-4] + ".png"):
            return self.file_path[:-4] + ".png"
        # If it does, add a number at the end, and iterate on the number until the name 
        # is unique
        else:
            file_path = self.file_path
            counter = 0
            while os.path.isfile(file_path[:-4] + ".png"):
                file_name_temp = str()
                file_name_temp = data_file_name[:-4] + " - " + str(counter) + ".png"
                file_path = os.path.join(self.save_directory,file_name_temp)
                counter += 1
            return file_path

### Other
    def show_figure(self):
        plt.draw()
        plt.show()

    def debug_print(self, message):
        if self.debug:
            print("\t" + str(message))
