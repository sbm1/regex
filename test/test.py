import sys

if ".." not in sys.path: sys.path.insert(0,"..")

from regex.parse_tree import build_tree
from regex.regex_parser import Regex
from regex.nfa import build_nfa, print_nfa

parser = Regex()

while 1:
    try:
        input_expression = input(">> ")
        parser.run(input_expression)
        tree = build_tree(parser.tree)
        print(tree)
        #print(list(iter(tree)))
        nfa = build_nfa(tree)
        print_nfa(nfa)
    except EOFError:
        break
