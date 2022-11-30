import datetime
import os
import csv
import time
"""
This class allows for saving of the collected data
"""

class DataLogger:
    file_name = str()

    is_file_open = False
    
    data_path = str()

    decimator = 1
    decimation_counter = 0

    flush_setpoint = 0
    flush_counter = 0

    generate_file_name = bool

    first_run = False       # Set to true when the first data is recorded 
    time_offset = int()     # Time when first data set was recorded 

    legend = list()
    data = list()

    # Initializer, opens the log file 
    def __init__(self, data_path , file_name = "" ,decimation = 1, flush_frequency = 1e3):
        self.data_path = data_path
        self.decimator = decimation
        self.flush_setpoint = flush_frequency
        
        self.create_file_name(data_path, file_name)
        
        self.file = open(self.file_name,'w+',newline='\n')
        self.is_file_open = True
        self.writer = csv.writer(self.file)

    # Generates a time stamped file name, or applies the provided the name
    # Ensures that the files do not overwrite eachother
    def create_file_name(self, data_path, file_name):
        # If the file name is not provided, get time and format it into a file name 
        if file_name == "":
            dt = datetime.datetime.now()
            file_name = str(dt.year) + "." + str(dt.month) + "." + str(dt.day) + "-" + str(dt.hour) + "." + str(dt.minute)
        else:
            file_name = str(file_name)
        file_path = os.path.join(data_path,file_name)

        # Check if the file exists if it does add an incremental number if the file exists
        counter = 1
        while os.path.isfile(file_path + ".csv"):
            file_name_temp = str()
            if file_name == "":
                file_name = str(dt.year) + "." + str(dt.month) + "." + str(dt.day) + "-" + str(dt.hour) + "." + str(dt.minute) + "-" + str(counter)
                file_path = os.path.join(data_path,file_name)
            else:
                file_name_temp = file_name + " - " + str(counter)
                file_path = os.path.join(data_path,file_name_temp)
            counter += 1
        # Add the extension name
        self.file_name =  file_path + ".csv"
    
    # Appends the data labels before they are written 
    def legend_append(self, legend_entry):
        self.legend += legend_entry

    # Writes the top row data labels 
    def write_legend(self):
        self.writer.writerow(["time"]+self.legend)
    
    # Appends data before it is written 
    def data_append(self, data):
        if isinstance(data, float) or isinstance(data, int):
            self.data.append(data)
        else:
            self.data += data
    
    # Writes the data, paying attantion to the decimator
    def write_data(self):
        if self.decimation_counter%self.decimator == 0:
            if not self.first_run:
                self.first_run = True
                self.time_offset = time.time()
            time_stamp = [str( (time.time()-self.time_offset))]
            self.writer.writerow(time_stamp+self.data)
            self.data = list()
            self.decimation_counter = 0
        self.decimation_counter += 1

        if self.flush_counter == self.flush_setpoint:
            self.file.flush()
            os.fsync(self.file)
            self.flush_counter = 0
        else:
            self.flush_counter += 1
        
    def close_file(self):
        self.is_file_open = False
        self.file.close()
    
    def get_file_path(self):
        return self.file_name
    
    def get_file_name(self):
        return os.path.basename(self.file_name)
    
    def get_full_path(self):
        return os.path.join(self.data_path, self.file_name)

    def __del__(self):
        if self.is_file_open:
            self.close_file()