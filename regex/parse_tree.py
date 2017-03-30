from itertools import chain

class ParseTree(object):
    '''
    Parse Tree built using Parser.root
    '''
    def __init__(self, v):
        '''
        @param v -- node value
        '''
        self.value = v
        self.children = []

    def __repr__(self, level=0):
        if self.value is None:
            output = "-" * level + "l{}".format(level) + "\n"
        else:
            output = "-" * level + self.value.strip() + "\n"

        for child in self.children:
            output += child.__repr__(level+1)

        return output

    def __iter__(self):
        for v in chain(*map(iter, self.children)):
            yield v
        yield self.value


def build_tree(t):
    '''
    Build a ParseTree using the list of lists generated from the parser

    @param t -- list

    @return -- ParseTree
    '''
    root = ParseTree(None)

    if isinstance(t, str):
        root = ParseTree(t)

    elif t is not None:
        root = ParseTree(None)
        for c in t:
            node = build_tree(c)
            root.children.append(node)

    return root
