output_types={
    "o":" output",
    "e":"  error",
    "h":"   help"
}

def output(output, type="o"):
    output = ["tfmt", output_types[type], str(output)]
    print(": ".join(output))
