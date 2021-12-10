from helpers import *
from cli import *
from re import compile, search

def tfmt(filename):
    print("filename: " + filename)
    try:
        f = open(filename + ".txt", "r")
    except:
        output("e", "filename: \"" + filename + "\" does not exist in the current directory")
        exit()

    lines = [l for l in f]

    # remove blank lines
    lines = [l for l in lines if l != "\n"]

    # remove added/created properties
    lines = [l for l in lines if l[0:6]!="      "]

    # remove numbers at the end of lines
    pattern = compile("\[1\]")
    for line in lines:
        if bool(search(pattern, line)):
            print(line)

    #print("".join(lines))
