import tkinter as tk

class RegexApp(tk.Tk):
    '''
    Visual for the Regex engine
    '''
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title('Regex')

        self._screenwidth = self.winfo_screenwidth()
        self._screenheight = self.winfo_screenheight()

        self.canvas = tk.Canvas(width=self._screenwidth, height=self._screenheight)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.configure(background='white')

    def clear(self, tag='all'):
        '''
        Clear the canvas. Defaults to all tags.

        @param tag -- str
        '''
        self.canvas.delete(tag)

    def create_nfa(self, nfa):
        '''
        Create a series of circles and lines to represent the given NFA.

        @param nfa -- NFA
        '''
        states = iter(nfa)

        self._state_radius = 10
        # state pos and state tuples in list
        self._state_pos = []

        ratio = 50
        x = ratio
        y = self._screenheight / 2

        self._create_state(x, y, 0)
        self._create_line(x/2, y, x-self._state_radius, y)
        self._state_pos.append( (0, (x, y)) )

    def _create_state(self, x, y, n):
        '''
        Create a circle to represent a state.

        @param x -- int, x position
        @param y -- int, y position
        @param n -- int, state number
        '''
        self.canvas.create_oval(x-self._state_radius, y-self._state_radius, 
                                x+self._state_radius, y+self._state_radius,
                                outline='black', fill='white', tags='state')
        self.canvas.create_text(x, y, text='s{}'.format(n))

    def _create_line(self, xA, yA, xB, yB):
        '''
        Join two states with a directional line.

        @param xA -- int, State A x pos
        @param yA -- int, State A y pos
        @param xB -- int, State B x pos
        @param yB -- int, State B y pos
        '''
        self.canvas.create_line((xA, yA), (xB, yB), smooth=True, arrow=tk.LAST)

    def _create_arc_line(self, xA, yA, xB, yB, d=100):
        '''
        Join two states with a curved directional line.

        @param xA -- int, State A x pos
        @param yA -- int, State A y pos
        @param xB -- int, State B x pos
        @param yB -- int, State B y pos
        @param d -- int, curve factor
        '''
