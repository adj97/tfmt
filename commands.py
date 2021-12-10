from helpers import *
from cli import *
from re import compile, search, sub

def tfmt(filename):
    print("filename: " + filename)
    try:
        f = open(filename + ".txt", "r")
    except:
        output("e", "filename: \"" + filename + "\" does not exist in the current directory")
        exit()

    patterns = {
        "digits" : compile("\[\d+\]"), # remove numbers at the end of lines"
        "newline" : compile("\n"), # remove newlines
    }

    # make and filter file
    lines = []
    for line in f:

        continue_conditions = [
            line == "\n", # ignore blank lines
            line[0:6]=="      ", # ignore added/created property lines
        ]

        if any(continue_conditions):
            continue
        else:
            line = sub(patterns["digits"], "", line)
            line = sub(patterns["newline"], "", line)
            
            lines.append(line)

    # need to do a frequency count of similar lines and print a table
