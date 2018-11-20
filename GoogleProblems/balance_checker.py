import re

def is_string_balanced(string):
    """
    Determines whether or not a string is "balanced", meaning if it has an equal number
    of open and closed parenthesis in the right order (e.g. "(())" as opposed to "((" or "))((")

    string: a string of only parethesis
    returns: True if the string is "balanced"
    """
    # check for the simplest bad case: wrong # or parenthesis
    if string.count("(") != string.count(")"):
        return False 
    # remove parethesis pairs until we can't, or there is no string left
    while len(string) > 0:
        # remove parenthesis pairs
        regexed = re.sub('\(\)', "", string)
        # if the string didn't change, it's invalid
        if regexed == string:
            return False
        # else iterate!
        string = regexed
    # empty string!
    return True