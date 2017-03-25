class NFA(object):
    '''
    Non-deterministic Finite Automata object using Thompson's algorithm.
    '''
    def __init__(self):
        '''
        Initialise the NFA's initial and current states
        '''
        self._initial_state = State()
        self._current_state = self._initial_state

    def get_initial_state(self):
        '''
        Returns the initial state

        @return -- State
        '''
        return self._initial_state

    def get_current_state(self):
        '''
        Returns the current state

        @return -- State
        '''
        return self._current_state

    def remove_initial_state(self):
        '''
        Removes the inital state from the NFA (for sub-nfas)
        '''
        self._initial_state = None

    def concat(self, s):
        '''
        Concatenates the basic symbols of an RE to the NFA

        @param s -- srting
        '''
        for c in s:
            next_state = State()
            e = Edge(self._current_state, next_state, c)

            self._current_state.add_outlink(e)
            next_state.add_inlink(e)

            self._current_state.non_accept()
            self._current_state = next_state
            self._current_state.make_accept()

    def concat_nfa(self, n):
        '''
        Concatenates an NFA to this NFA

        @param n -- nfa
        '''
        epsilon = Edge(self._current_state, n.get_initial_state(), 'E')
        self._current_state.add_outlink(epsilon)
        n.get_initial_state().add_inlink(epsilon)

        self._current_state.non_accept()
        self._current_state = n.get_current_state()
        self._current_state.make_accept()

    def create_or_branch(self, n):
        '''
        Create a branch coming from the initial state when or occurs and insert the alternative nfa. 

        @param n -- nfa
        '''
        epsilon = Edge(self._initial_state, n.get_initial_state(), 'E')
        self._initial_state.add_outlink(epsilon)
        n.get_initial_state().add_inlink(epsilon)

        epsilon = Edge(n.get_current_state(), self._current_state, 'E')
        n.get_current_state.add_outlink(epsilon)
        self._current_state.add_inlink(epsilon)

        n.get_current_state().non_accept()

    def kleene_star(self, c):
        '''
        Deals with N(s*) by adding new links.

        @param c -- edge char
        '''
        e = Edge(self._current_state, self._current_state, c)
        self._current_state.add_inlink(e)
        self._current_state.add_outlink(e)

        epsilon = Edge(self._current_state.source_of(c), self._current_state, 'E')
        self._current_state.add_inlink(epsilon)
        self._current_satte.source_of(c).add_outlink(epsilon)

    def kleene_star_nfa(self, n):
        '''
        Deals with N(s)*

        @param n -- nfa
        '''
        epsilon = Edge(self._current_state, n.get_initial_state(), 'E')
        self._current_state.add_outlink(epsilon)
        n.get_initial_state().add_inlink(epsilon)

        epsilon = Edge(n.get_current_state, n.get_initial_state(), 'E')
        n.get_current_state.add_outlink(epsilon)
        n.get_initial_state().add_inlink(epsilon)

        next_state = State()

        epsilon = Edge(self._current_state, next_state, 'E')
        n.get_current_state.add_outlink(epsilon)
        next_state.add_inlink(epsilon)

        self._current_state.non_accept()
        self._current_state = next_state
        self._current_state.make_accept()


class State(object):
    '''
    State object. How each State of the Non-deterministic Finite Automata is defined.
    '''
    def __init__(self):
        '''
        Initialise the Sate with false accept state and empty links
        '''
        self._accept_state = False
        self._outlinks = []
        self._inlinks = []

    def is_accept(self):
        '''
        @return -- is the State an accept state
        '''
        return self._accept_state

    def make_accept(self):
        '''
        Sets the accept state to True
        '''
        self._accept_state = True

    def non_accept(self):
        '''
        Sets the accept state to False
        '''
        self._accept_state = False

    def get_outlinks(self):
        '''
        @return -- State's out links
        '''
        return self._outlinks

    def add_outlink(self, e):
        '''
        Adds an new out link to the state
        '''
        self._outlinks.append(e)

    def get_inlinks(self):
        '''
        @return -- State's in links
        '''
        return self._inlinks

    def add_inlink(self, e):
        '''
        Adds an new in link to the state
        '''
        self._inlinks.append(e)

    def contains_outlink(self, c):
        '''
        Returns true if the State contains the out link with a given label

        @param c -- edge char

        @return -- Boolean
        '''
        for edge in self._outlinks:
            if edge.get_label() == c:
                return True
        return False

    def next_state(self, c):
        '''
        Gives the next state with edge c

        @param -- edge char

        @return -- State
        '''
        for edge in self._outlinks:
            if edge.get_label() == c:
                return edge.get_target()
        return State()

    def source_of(self, c):
        '''
        Returns the source State with given edge

        @param c -- edge char

        @return -- State
        '''
        for edge in self._inlinks:
            if edge.get_label() == c:
                return edge.get_source()
        return State()

    def remove_outlink(self, c):
        '''
        Removes Edges from the out links of the State if they're labelled c

        @param c -- edge char
        '''
        for edge in self._outlinks:
            if edge.get_label() == c:
                self._outlinks.remove(edge)


class Edge(object):
    '''
    Edge object. Describes the link between States
    '''
    def __init__(self, source, target, label):
        '''
        @param source -- source State
        @param target -- target State
        @param label -- edge character
        '''
        self._edge = source, target, label

    def get_source(self):
        '''
        @return -- source State
        '''
        return self._edge[0]

    def get_target(self):
        '''
        @return -- target State
        '''
        return self._edge[1]

    def get_label(self):
        '''
        @return -- edge char
        '''
        return self._edge[2]


def build_nfa(regex):
    '''
    Function for building a Non-deterministic Finite Automata from a regeular expression.

    @param regex -- String

    @return -- NFA
    '''
    nfa = NFA()

    exprs, sub_exprs = split_regex(regex)

    for i, e in enumerate(exprs):
        if isinstance(e, str):
            if '|' in e:
                create_or(nfa, e)
            elif '*' in e:
                star(nfa, e)
        else:
            sub_nfa = build_nfa(sub_exprs[e])
            # need to check if next element is *
            # if so then kleene_star_nfa() else concat_nfa()
            if i+1 != len(exprs) and exprs[i+1][0] is '*':
                nfa.kleene_star_nfa(sub_nfa)
            else:
                nfa.concat_nfa(sub_nfa)

    return nfa

def create_or(nfa, exprs):
    '''
    Create or branch for the given NFA using a list of exprs split by '|'
    e.g. : 'a|b' -> ['a', 'b']

    @param nfa -- NFA
    @param exprs -- list
    '''
    sub_nfa = NFA()
    exprs = exprs.split('|')

    if '*' in exprs[0]:
        star(sub_nfa, exprs[0])
    else:
        sub_nfa.concat(exprs[0])

    for i in range(1, len(exprs)):
        if '*' in exprs[i]:
            temp_nfa = NFA()
            star(temp_nfa, exprs[i])
        else:
            temp_nfa = NFA()
            temp_nfa.concat(exprs[i])
        sub_nfa.create_or_branch(temp_nfa)

    nfa.concat_nfa(sub_nfa)

def star(nfa, exprs):
    '''
    Add the elements of exprs to the NFA and kleene star certain chars depending on their position in exprs.
    e.g. : 'aa*bb' -> ['aa', 'bb']
           length of exprs is 2 so 1 kleene star to be applied (all but the last element)
           if the first element is '' then the kleene star has been applied to the previous sub_nfa
           if the last element is '' then apply the kleene star the previous char as normal and ignore as normal

    @param nfa -- NFA
    @param exprs -- list
    '''
    exprs = exprs.split('*')
    num_stars = len(exprs) - 1
    i = 0

    for e in exprs:
        if e is not '':
            nfa.concat(e)
            if i < num_stars:
                nfa.kleene_star(e[-1])
        i = i+1

def split_regex(regex):
    '''
    Split the regular expression into parts to be made into an nfa and then merged together.

    @param regex -- String

    @return -- iterator
    '''
    output = []
    bracket = False
    sub_part = ""
    sub_parts_dict = {}
    i = 0

    for r in regex:
        if bracket and r is not ')':
            sub_part = sub_part + r
        elif r is '(':
            if sub_part is not "":
                output.append(sub_part)
            sub_part = ""
            bracket = True
        elif r is ')':
            sub_parts_dict[i] = sub_part
            sub_part = ""
            bracket = False
            output.append(i)
            i = i+1
        else:
            sub_part = sub_part + r

    if sub_part is not "":
        output.append(sub_part)
    
    return output, sub_parts_dict
