epsilon = 'E'

class NFA(object):
    '''
    Non-deterministic Finite Automaton object
    '''
    def __init__(self, tree):
        '''
        Initialise the NFA using a ParseTree

        @param tree -- ParseTree
        '''
        self._states = build_nfa(tree)
        self.assign_states()

    def __repr__(self):
        output = ""
        for state in self._states:
            for s, c in state.get_out_links():
                output += "state{} -- {} --> state{}\n".format(state.state_no, c, s.state_no)
        return output

    def __iter__(self):
        '''
        Iterates thru each state's outgoing links: ( state, linked state, char linking states )
        '''
        for state in self._states:
            for s, c in state.get_out_links():
                yield state, s, c

    def assign_states(self):
        '''
        Assign state numbers to each state in the automaton.
        '''
        num_states = 0

        for state in self._states:
            if state.state_no is None:
                state.state_no = num_states
                num_states += 1


class State(object):
    '''
    Each state of an NFA.
    Contains lists of links out and in to the connecting states in the NFA.
    '''
    def __init__(self):
        '''
        Initialise state.
        Vars: accept    -- whether the state is an accept state
              out_links -- list of State objects that this state has an outward connection to
              in_links  -- list of State objects that this state has an outward connection to
              state_no  -- number of the state in the NFA (initially not set)
        '''
        self._accept = False
        self._out_links = []
        self._in_links = []
        self.state_no = None

    def get_out_links(self):
        '''
        @return -- list
        '''
        return self._out_links

    def get_in_links(self):
        '''
        @return -- list
        '''
        return self._in_links

    def get_accept(self):
        '''
        @return -- boolean
        '''
        return self._accept

    def add_out_link(self, edge):
        '''
        Adds a given edge tuple (state, char) to the state's outlinks
        @param edge -- tuple
        '''
        self._out_links.append(edge)

    def add_in_link(self, edge):
        '''
        Adds a given edge tuple (state, char) to the state's inlinks
        @param edge -- tuple
        '''
        self._in_links.append(edge)


def build_nfa(tree):
    '''
    Build an Non-deterministic Finite Automata from a ParseTree.
    An NFA is represented by a list of State objects in the NFA

    @param tree -- ParseTree

    @return -- list
    '''
    # if the node has value None then the node's children need to be cycled through
    if tree.value is None:
        # sub NFAs will be built from the children of each node
        sub_nfas = []

        for child in tree.children:
            sub_nfa = build_nfa(child)
            # if there is a sub NFA from this branch it is appended
            if sub_nfa:
                sub_nfas.append(sub_nfa)

        # now check what the sub NFA list contains and deal with each applicably

        # for or nodes the list will look like [ nfa, '|', nfa ]
        if '|' in sub_nfas and len(sub_nfas) == 3:
            return create_or_branch(sub_nfas[0], sub_nfas[2])

        # kleene star nodes will have [ nfa, '*' ]
        elif '*' in sub_nfas and len(sub_nfas) == 2:
            return kleene_star(sub_nfas[0])

        # '+' will be the same but has different application
        elif '+' in sub_nfas and len(sub_nfas) == 2:
            return plus(sub_nfas[0])

        # bracket nodes will be [ '(', nfa, ')', '*' ]
        # the final star may not be there so both sizes will need to be checked
        elif '(' in sub_nfas and (len(sub_nfas) == 4 or len(sub_nfas) == 3):
            if '*' in sub_nfas:
                return kleene_star(sub_nfas[1])
            elif '+' in sub_nfas:
                return plus(sub_nfas[1])
            else:
                return sub_nfas[1]
        
        # if the list is size two then the node contains two sub NFAs that need to be concatenated
        elif len(sub_nfas) == 2:
            return concat(sub_nfas[0], sub_nfas[1])

        # size is 1 could contain chars * or +
        elif len(sub_nfas) == 1:
            return sub_nfas[0]
        
        # otherwise return (empty list)
        else:
            return sub_nfas

    # if not None then op or char
    else:
        # operators should simply be returned
        if tree.value in ['|', '*', '+', '(', ')']:
            return tree.value

        # if chars then build a sub NFA e.g. a -> s0--a-->s1
        else:
            nfa = []
            
            init_state = State()
            final_state = State()

            final_state.add_in_link( (init_state, tree.value) )
            init_state.add_out_link( (final_state, tree.value) )

            nfa.append(init_state)
            nfa.append(final_state)

            return nfa

def concat(nfa1, nfa2):
    '''
    Concatenate two NFAs by adding links between the final state of one and the initial state of the other.

    @param nfa1 -- list
    @param nfa2 -- list

    @return list
    '''
    nfa1[-1].add_out_link( (nfa2[0], epsilon) )
    nfa2[0].add_in_link( (nfa1[-1], epsilon) )

    return nfa1 + nfa2

def create_or_branch(nfa1, nfa2):
    '''
    Create or branch by adding a new final and init state, 
    having seperate paths from the init to the final through the two NFAs.

    @param nfa1 -- list
    @param nfa2 -- list

    @return list
    '''
    new_init_state = State()
    new_init_state.add_out_link( (nfa1[0], epsilon) )
    new_init_state.add_out_link( (nfa2[0], epsilon) )

    new_final_state = State()
    new_final_state.add_in_link( (nfa1[-1], epsilon) )
    new_final_state.add_in_link( (nfa2[-1], epsilon) )

    nfa1[0].add_in_link( (new_init_state, epsilon) )
    nfa2[0].add_in_link( (new_init_state, epsilon) )

    nfa1[-1].add_out_link( (new_final_state, epsilon) )
    nfa2[-1].add_out_link( (new_final_state, epsilon) )

    return [new_init_state] + nfa1 + nfa2 + [new_final_state]

def kleene_star(nfa):
    '''
    Implement kleene star by creating new init and final states.
    Link the new init to the new final as well as the init of the NFA.
    Link the final of the NFA to the new final as well as to the init of the NFA.
    
    @param nfa -- list

    @return list
    '''
    new_final_state = State()
    new_final_state.add_in_link( (nfa[-1], epsilon) )

    new_init_state = State()
    new_init_state.add_out_link( (nfa[0], epsilon) )

    new_init_state.add_out_link( (new_final_state, epsilon) )
    new_final_state.add_in_link( (new_init_state, epsilon) )

    nfa[-1].add_out_link( (nfa[0], epsilon) )
    nfa[0].add_in_link( (nfa[-1], epsilon) )

    nfa[-1].add_out_link( (new_final_state, epsilon) )
    nfa[0].add_in_link( (new_init_state, epsilon) )

    return [new_init_state] + nfa + [new_final_state]

def plus(nfa):
    '''
    Similar to kleene star, leaving out link from init state to new final state

    @param nfa -- list

    @return list
    '''
    new_final_state = State()
    new_final_state.add_in_link( (nfa[-1], epsilon) )

    new_init_state = State()
    new_init_state.add_out_link( (nfa[0], epsilon) )

    nfa[-1].add_out_link( (nfa[0], epsilon) )
    nfa[0].add_in_link( (nfa[-1], epsilon) )

    nfa[-1].add_out_link( (new_final_state, epsilon) )
    nfa[0].add_in_link( (new_init_state, epsilon) )

    return [new_init_state] + nfa + [new_final_state]
