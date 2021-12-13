from re import compile

output_types={
    "o":" output",
    "e":"  error",
    "h":"   help"
}

def output(text, type="o"):
    print(cli_format(text, type))

def input_fmt(text, type="h"):
    input(cli_format(text, type))

def cli_format(text, type):
    return ": ".join(["tfmt", output_types[type], str(text)])

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
    
# Continue conditions does some data clensing according to the following:
# Boolean array where the following if statement will ignore a line if true
# [0] - blank lines
# [1] - added/created property lines
# [2] - terraform std output
# [3] - terraform summary line
def get_continue_conditions(line):
    return [
        line == "\n", 
        line[0:6]==" "*6, 
        "Terraform will perform the following actions:" in line,
        any(substring in line for substring in ["Plan: "," to add, "," to change, "," to destroy"])
    ]

def yesno():
    try:
        if input_fmt("[Y/n] ").lower() in ["n", "no"]:
            return False
        else:
            return True
    except AttributeError as e:
        # Probably default enter
        return True

summary = []

def printlog(text):
    print(text)
    summary.append(text)