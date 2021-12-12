from helpers import *
from cli import *
from re import compile, sub
from tabulate import tabulate
from copy import copy


def tfmt(filename_input):
    # Check filename input
    arg_decomp = filename_input.split(".")
    if len(arg_decomp)==1:
        if arg_decomp[0] == "clip":
            output("Reading from clipboard")
            raise Exception("Feature not supported yet")
        else:
            # Assume txt file
            filename = filename_input + ".txt"
            output("Summarising file: " + filename)
    elif len(arg_decomp)==2:
        name = arg_decomp[0]
        extension = arg_decomp[1]
        if extension != "txt": 
            raise Exception("Unsupported file type: \"" + extension + "\"")
        else:
            filename = name + "." + extension
    else:
        raise Exception("Unrecognised input: \"" + filename_input + "\"")

    # Read the file
    try:
        f = [l for l in open(filename, "r")]
    except:
        output("filename: \"" + filename + "\" does not exist in the current directory", "e")
        exit()

    # Check for some terraform stuff
    tf_strings = [
        "Terraform will perform the following actions:",
        "Plan","add","change","destroy", "pigz"
    ]
    check = 100 * sum([checkstring in ''.join(f) for checkstring in tf_strings]) / len(tf_strings)
    if check != 100:
        if check == 0:
            raise Exception("I'm pretty sure {0} isn't terraform".format(filename + ".txt"))
        else:
            output("This is {0}% a tf output file ...".format(check), "h")
            output("I'm happy to carry on, but I might not do a great job if this isn't a tf output file", "h")
            output("Do you want me to carry on anyway?", "h")

    # Patterns array does some data clensing according to the following:
    # "digits"  - remove numbers at the end of lines"
    # "newline" - remove newlines
    # "azs"     - merge all the availability zone lines together
    # "plus"    - remove plus sign at the start
    patterns = {
        "digits" : ["\[\d+\]", ""], 
        "newline" : ["\\n", ""],
        "azs" : ["_az_\d", "_az_x"], 
        "plus" : ["\+ ", ""]
    }

    for p in patterns:
        patterns[p][0] = compile(patterns[p][0])

    # construct and filter lines array
    lines = []
    for line in f:

        # Continue conditions does some data clensing according to the following:
        # Boolean array where the following if statement will ignore a line if true
        # [0] - blank lines
        # [1] - added/created property lines
        # [2] - terraform std output
        # [3] - terraform summary line
        continue_conditions = [
            line == "\n", 
            line[0:6]==" "*6, 
            "Terraform will perform the following actions:" in line,
            any(substring in line for substring in ["Plan: "," to add, "," to change, "," to destroy"])
        ]

        # skip or keep each line
        if any(continue_conditions):
            if continue_conditions[3]:
                print("\n" + line)
            continue
        else:
            for p in patterns:
                line = sub(*patterns[p], line)

            lines.append(line)

    # Frequency count array
    groups = [[line for line in lines if line==compare_line] for i, compare_line in enumerate(lines) if compare_line not in lines[:i]]

    # Output
    headers = ["Resource (grouped)", "Count"]
    data = [[group[0], len(group)] for group in groups]
    print("\n" + tabulate(data, headers) + "\n")
