from sys import argv
from cli import *
from helpers import *
from commands import tfmt

if __name__ == "__main__":

    args = [a for a in argv if "main.py" not in a]

    # empty args
    if len(args) == 0:
        help()
        exit()
    elif len(args) == 1:
        # one parameter function only
        try:
            tfmt(args[0])
            output("Completed")
        except Exception as e:
            output("Aborted")
            output(e, "e")
    else:
        output("Unrecognised arguments: " + "\"" + " ".join(args) + "\"", "e")
        help()
