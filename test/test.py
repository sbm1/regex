import sys

if ".." not in sys.path: sys.path.insert(0,"..")

from regex.parse_tree import build_tree
from regex.regex_parser import Regex

parser = Regex()

while 1:
    try:
        input_expression = input(">> ")
        parser.run(input_expression)
        tree = build_tree(parser.tree)
        print(tree)
        print(list(iter(tree)))
    except EOFError:
        break
