import argparse
from brainfrick import *
import re

# Set up expected arguments
parser = argparse.ArgumentParser()

# Mandatory paramaters
parser.add_argument('code', help='brainfuck code or the path to a file containing brainfuck code.')

# Optional parameters
parser.add_argument('--cells', help='set the number of cells. Defaults to 8.', default=8)
args = parser.parse_args()

# Build a BrainfuckMachine with custom parameters (if given)
bfm = BrainfuckMachine(cells=args.cells)

# Instantiate the interpreter
bfi = BInterpreter(machine=bfm)


# Try to open a file, if it is not found, assume the 'code' argument was brainfuck code.
try:
    s = open(args.code).read()
    code = list(BLexer.lex(s))
    bfi.interpret_code(code)

except Exception as e:
    expects = re.compile("^[^><\+-\.,\[\]]+$")
    if expects.match(args.code):
        print("No brainfuck code detected, exiting.")
        exit(0)
    else:
        code = list(BLexer.lex(args.code))
        bfi.interpret_code(code)
    
    