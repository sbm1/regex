from ply import lex, yacc

class Parser(object):
    '''
    Base class for a lexer/parser
    '''
    tokens = ()
    precedence = ()

    def __init__(self):
        self.tree = None
        
        lex.lex(module=self)
        yacc.yacc(module=self)
        
    def run(self, s):
        '''
        Run the parser on input s
        
        @param s -- String input
        '''
        yacc.parse(s)
        

class Regex(Parser):
    # tokens
    tokens = (
            'ID', 
            'ASTERIX', 
            'PLUS', 
            'LBRACKET', 
            'RBRACKET', 
            'OR', 
            'LBRACE', 
            'RBRACE', 
            'DASH', 
            'NOT', 
            'EMPTY'
            )

    # token definitions (using RE)
    t_ASTERIX = r'\*'
    t_PLUS = r'\+'
    t_LBRACKET = r'\('
    t_RBRACKET = r'\)'
    t_OR = r'\|'
    t_LBRACE = r'\['
    t_RBRACE = r'\]'
    t_DASH = r'\-'
    t_NOT = r'\^'

    # define more complex tokens
    def t_ID(self, t):
        r'[a-zA-Z0-9.]'
        t.type = 'ID'
        return t

    def t_EMPTY(self, t):
        r'\{\}'
        t.type = 'EMPTY'
        return t

    def t_error(self, t):
        print("Illegal characters!")
        t.lexer.skip(1)

    precedence = (
            ('left', 'OR'),
            ('left', 'PLUS', 'ASTERIX'),
            ('left', 'LBRACKET', 'RBRACKET')
            )

    # grammar defined below
    def p_grammar(self, p):
        '''
        grammar : regex
        '''
        self.tree = p[1:]

    def p_regex(self, p):
        '''
        regex : expression
              | empty
        '''
        p[0] = p[1:]

    def p_expression(self, p):
        '''
        expression : expression expr
                   | expr
        '''
        p[0] = p[1:]

    def p_expr(self, p):
        '''
        expr : bracketexpr
             | orexpr
             | id
        '''
        p[0] = p[1:]

    def p_bracketexpr(self, p):
        '''
        bracketexpr : LBRACKET regex RBRACKET symbol
        '''
        p[0] = p[1:]

    def p_orexpr(self, p):
        '''
        orexpr : expr OR expr
        '''
        p[0] = p[1:]

    def p_id(self, p):
        '''
        id : ID symbol
           | range symbol
           | EMPTY
        '''
        p[0] = p[1:]

    def p_range(self, p):
        '''
        range : LBRACE not subranges RBRACE
        '''
        p[0] = p[1:]

    def p_not(self, p):
        '''
        not : NOT
            | empty
        '''
        p[0] = p[1:]
    
    def p_subranges(self, p):
        '''
        subranges : subranges subrange
                  | subrange
        '''
        p[0] = p[1:]

    def p_subrange(self, p):
        '''
        subrange : ID
                 | ID DASH ID
        '''
        p[0] = p[1:]

    def p_symbol(self, p):
        '''
        symbol : ASTERIX
               | PLUS
               | empty
        '''
        p[0] = p[1:]

    def p_empty(self, p):
        '''
        empty : 
        '''
        p[0] = None

    def p_error(self, p):
        print("Syntax error found!")
