from helpers import get_continue_conditions, patterns, output, input_fmt, yesno, printlog, summary
from cli import *
from re import sub
from tabulate import tabulate
from copy import copy
import pyperclip


def tfmt(filename_input):
    # Check filename input
    arg_decomp = filename_input.split(".")
    if len(arg_decomp)==1:
        if arg_decomp[0] == "clip":
            output("Reading from clipboard")
            clipboard = True
            cliptext = pyperclip.paste()
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
    if not clipboard:
        try:
            f = [l for l in open(filename, "r")]
        except:
            output("filename: \"" + filename + "\" does not exist in the current directory", "e")
            exit()
    else:
        f = cliptext.split("\n")

    # Check for some terraform stuff
    tf_strings = [
        "Terraform will perform the following actions:",
        "Plan","add","change","destroy"
    ]
    check = 100 * sum([checkstring in ''.join(f) for checkstring in tf_strings]) / len(tf_strings)
    if check != 100:
        if check == 0:
            raise Exception("I'm pretty sure {0} isn't terraform".format(filename + ".txt"))
        else:
            output("This is {0}% a tf output file ...".format(check), "h")
            output("I'm happy to carry on, but I might not do a great job if this isn't a tf output file", "h")
            output("Do you want me to carry on anyway?", "h")
            if not yesno():
                output("Stopping")
                exit()

    # construct and filter lines array
    lines = []
    for line in f:

        continue_conditions = get_continue_conditions(line)

        # skip or keep each line
        if any(continue_conditions):
            if continue_conditions[3]:
                printlog("\n" + line)
            continue
        else:
            for p in patterns:
                line = sub(*patterns[p], line)

            lines.append(line)

    # Frequency count array
    groups = [[line for line in lines if line==compare_line] for i, compare_line in enumerate(lines) if compare_line not in lines[:i]]

    # Output
    headers = ["Count", "Resource Changed (grouped)"]
    data = [[len(group), group[0]] for group in groups]
    printlog("\n" + tabulate(data, headers) + "\n")

    # Copy to clipboard
    output("Copy to clipboard?")
    if yesno():
        pyperclip.copy(''.join(summary))