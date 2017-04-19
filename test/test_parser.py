import sys

if ".." not in sys.path: sys.path.insert(0,"..")

from regex.regex_parser import Regex

parser = Regex()

while 1:
    try:
        input_expression = input("RE:\n>> ")
        parser.run(input_expression)
        print(parser.tree)
    except EOFError:
        break
