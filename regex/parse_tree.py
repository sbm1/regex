class RegexNode(object):
    '''
    Node object in a regex tree.
    '''
    def __init__(self, t, c, p=None):
        '''
        Initialise the Node

        @param t -- the rule applied to this node
        @param c -- list of children of this node
        @param p -- the parent of this node
        '''
        self._node_type = t
        self._children = c
        self._parent = p

    def __repr__(self, level=0):
        ret = "-" * level + self._node_type.strip() + "\n"
        for child in self._children:
            if isinstance(child, RegexNode):
                ret += child.__repr__(level+1)
            elif child is not None:
                ret += "-" * (level+1) + child.strip() + "\n"
        return ret

    def get_children(self):
        '''
        Return the list of children for this node

        @return -- list of nodes or elements
        '''
        return self._children

    def get_type(self):
        '''
        Return the type of the node (i.e. the rule for this node)

        @return -- String describing the rule for this node
        '''
        return self._node_type

    def get_parent(self):
        '''
        Return the parent of this node

        @return -- parent RegexNode
        '''
        return self._parent

    def set_parent(self, p):
        '''
        Set the parent node of this node

        @param parent -- RegexNode that is the parent for this node
        '''
        self._parent = p

class ParseTree(object):
    '''
    Parse Tree containing root RegexNode
    '''
    def __init__(self, root):
        '''
        root -- Root RegexNode
        '''
        self.root = root
        self.set_parents(root)

    def set_parents(self, node):
        '''
        Traverse the tree assigning each nodes parent

        @param node -- the current node
        '''
        # TODO: time complexity improvements?
        for child in node.get_children():
            if isinstance(child, RegexNode):
                child.set_parent(node)
                self.set_parents(child)

    def print_tree(self):
        '''
        Print tree
        '''
        print(self.root)
