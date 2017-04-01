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
        Input list of State objects.

        @param nfa -- list
        '''
        self._num_states = len(nfa)

    def _create_state(self, x, y, n):
        '''
        Create a circle to represent a state.

        @param x -- int, x position
        @param y -- int, y position
        @param n -- int, state number
        '''

    def _create_line(self, xA, yA, xB, yB):
        '''
        Join two states with a directional line.

        @param xA -- int, State A x pos
        @param yA -- int, State A y pos
        @param xB -- int, State B x pos
        @param yB -- int, State B y pos
        '''

    def _create_arc_line(self, xA, yA, xB, yB, d=100):
        '''
        Join two states with a curved directional line.

        @param xA -- int, State A x pos
        @param yA -- int, State A y pos
        @param xB -- int, State B x pos
        @param yB -- int, State B y pos
        @param d -- int, curve factor
        '''
