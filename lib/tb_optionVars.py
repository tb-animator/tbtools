__author__ = 'user'
import pymel.core as pm

class optionVar_utils():
    def __init__(self):
        pass

    @staticmethod
    def set_option_var(variable, value):
        pm.optionVar(stringValue=(variable, value))


    @staticmethod
    def get_option_var(variable):
        if not pm.optionVar[variable]:
            pm.optionVar(stringValue=(variable, "None"))
        return pm.optionVar.get(variable, False)

    @staticmethod
    # list from option var
    def cycleOption(option_name="", full_list=[], current=int(), default=""):
        # get list from optionvar array
        optionVar_list = pm.optionVar.get(option_name, [default])
        if not optionVar_list:
            optionVar_list = [default]
        print optionVar_list
        # find the current index in the full list
        current_name = full_list[current]
        print current_name
        print

        # check if the current name is in our option var list
        if current_name in optionVar_list:
            index = optionVar_list.index(current_name) + 1
            print "index", index
            # loop around the list
            name = optionVar_list[index % len(optionVar_list)]

        else:
            print "current value not in option var list, set to first"
            name = optionVar_list[0]
        index = full_list.index(name)
        print name, index
        return index, name

# size, type, dimensions = getImageData(x)