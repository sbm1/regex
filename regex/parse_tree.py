from itertools import chain


class ParseTree(object):
    """
    Parse Tree built using Parser.root
    """

    def __init__(self, v):
        """
        @param v -- node value
        """
        self.value = v
        self.children = []

    def __repr__(self, level=0):
        if self.value is None:
            output = "-" * level + "l{}".format(level) + "\n"
        else:
            output = "-" * level + self.value.strip() + "\n"

        for child in self.children:
            output += child.__repr__(level + 1)

        return output

    def __iter__(self):
        for v in chain(*map(iter, self.children)):
            yield v
        yield self.value


def build_tree(t):
    """
    Build a ParseTree using the list of lists generated from the parser

    @param t -- list

    @return -- ParseTree
    """
    root = ParseTree(None)

    if isinstance(t, str):
        root = ParseTree(t)

    elif t is not None:
        root = ParseTree(None)
        for c in t:
            if c is '[':
                node = build_tree(range_to_id(t))
                root.children.append(node)
                break
            else:
                node = build_tree(c)
                root.children.append(node)

    return root


def range_to_id(t):
    """
    Unnest the elements of the range and concatenate them to a string.
    E.g. ['[', ['^'], [['a', '-', 'z']], ']'] -> "[^a-z]"

    @param t -- list

    @return str
    """
    ret = ""

    for c in t:
        while isinstance(c, list):
            c = range_to_id(c)
        if isinstance(c, str):
            ret += c

    return ret
