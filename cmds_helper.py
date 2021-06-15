#####################################
# HELPER FUNCTIONS FOR THE COMMANDS #
#####################################


def args_to_array(value, min_args):
    """
    Converts a string of arguments seperated by ";" to a list of values
    """
    value = value.split(';')

    if len(value) < min_args:
        raise Exception("not enough arguments")

    return value


def all_to_int(array):
    """
    Used to convert an array of string args to ints
    """
    
    return [int(x.strip()) for x in array]
