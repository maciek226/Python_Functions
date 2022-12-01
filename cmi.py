
# How to restrict some options? 

class CMI:
    
    selection_out_of_range_message = "Selection out of range. Please try again."
    selection_not_number = "Please enter a number. Please try again."
    
    cancel_command = "cnc"
    exit_command = "exit"
        
    def __init__(self):
        pass
    
    def select_option(self, options, tabs = 0):
        cc = 0
        for option in options:
            print("\t"*tabs + str(cc) +" - " + option)
            cc += 1
        cc -= 1
        return self._get_selection(cc, tabs)
            
    def _get_selection(self, cc, tabs):
        while True:
            selection = input("\n\t"*(tabs) + "Please select an option: ")
            if selection.isnumeric():
                if int(selection) <= cc:
                    return int(selection)
                else:
                    print("\t"*(tabs+1) + self.selection_out_of_range_message)
            elif selection == self.cancel_command:
                return "cnc"
            elif selection == self.exit_command:
                return "exit"
            else:
                print("\t"*(tabs+1) + self.selection_not_number)
    
    def get_numeric_input(self, message, tabs = 0):
        while True:
            selection = input("\t"*(tabs) + message)
            if selection.isnumeric():
                return int(selection)
            elif selection == self.cancel_command:
                return "cnc"
            else:
                print("\t"*(tabs+1) + self.selection_not_number)
    
    def string_input(self, message, tabs = 0):
        return input("\t"*(tabs) + message)