import sys

if ".." not in sys.path: sys.path.insert(0,"..")

from regex.parse_tree import ParseTree
from regex.regex_parser import Regex

parser = Regex()

while 1:
    try:
        input_expression = input(">> ")
        parser.run(input_expression)
        tree = ParseTree(parser.root)
        tree.print_tree()
    except EOFError:
        break
