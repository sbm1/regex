import sys
import re

if ".." not in sys.path: sys.path.insert(0,"..")

from regex.parse_tree import build_tree
from regex.regex_parser import Regex
from regex.nfa import NFA
from regex.app import RegexApp, create_nfa

parser = Regex()

while 1:
    try:
        input_expression = input("RE:\n>> ")
        parser.run(input_expression)

        if not parser.error:
            tree = build_tree(parser.tree)
            #print(tree)
            #print(list(iter(tree)))
            nfa = NFA(tree)
            #print(nfa)

            test_str = input("Test:\n>> ")
            p = re.compile(input_expression)
            m = p.match(test_str)

            if m is None:
                print("Reject.")
            elif m.group() is test_str:
                print("Accept.")
            else:
                print("Reject.")
        
            app = RegexApp()
            create_nfa(app, nfa)
            app.mainloop()
    except EOFError:
        break
