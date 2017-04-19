import tkinter as tk
from parse_tree import build_tree
from regex_parser import Regex
from nfa import NFA
import re

class RegexApp(tk.Tk):
    '''
    Visual for the Regex engine
    '''
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title('Regex')

        self.parser = Regex()

        self.screenwidth = self.winfo_screenwidth()
        self.screenheight = self.winfo_screenheight()

        self.label1 = tk.Label(self, text='Regular Expression: ')
        self.label1.pack()
        self.regex_entry = tk.Entry(self, width=50)
        self.regex_entry.pack(padx=5, pady=5)
        self.regex_entry.focus()

        self.label2 = tk.Label(self, text='Test String: ')
        self.label2.pack()
        self.test_entry = tk.Entry(self, width=50)
        self.test_entry.pack(padx=5, pady=5)

        self.bind('<Return>', (lambda event: self.regex()))

        self.button = tk.Button(self, width=25, bd=3, text='Submit', command=self.regex)
        self.button.pack(padx=5, pady=5)

        self.exit_button = tk.Button(self, width=25, bd=3, text='Exit', command=self.destroy)
        self.exit_button.pack(padx=5, pady=5)

        self.canvas = tk.Canvas(self, width=self.screenwidth, height=self.screenheight-200)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.configure(background='white')

        # radius of states
        self.state_rad = 20
        self.ratio = 100

    def regex(self):
        '''
        Main regex function.
        '''
        self.clear()

        usr_input = self.regex_entry.get()
        test_input = self.test_entry.get()
        
        if len(usr_input) > 0:
            self.parser.run(usr_input)

            if not self.parser.error:
                if len(test_input) > 0:
                    p = re.compile(usr_input)
                    m = p.match(test_input)
                    
                    if m is None:
                        self.canvas.create_text(self.screenwidth/2, 10, text='Reject: {}'.format(test_input), tags='text')
                    elif m.group() is test_input:
                        self.canvas.create_text(self.screenwidth/2, 10, text='Accept: {}'.format(test_input), tags='text')
                    else:
                        self.canvas.create_text(self.screenwidth/2, 10, text='Reject: {}'.format(test_input), tags='text')

                tree = build_tree(self.parser.tree)
                nfa = NFA(tree)
                create_nfa(self, nfa)

    def clear(self, tag='all'):
        '''
        Clear the canvas. Defaults to all tags.

        @param tag -- str
        '''
        self.canvas.delete(tag)

    def create_state(self, x, y, n):
        '''
        Create a circle to represent a state.

        @param x -- int, x position
        @param y -- int, y position
        @param n -- int, state number
        '''
        self.canvas.create_oval(x-self.state_rad, y-self.state_rad, 
                                x+self.state_rad, y+self.state_rad,
                                outline='black', fill='white', tags='state')
        self.canvas.create_text(x, y, text='s{}'.format(n), tags='text')

    def create_final_state(self, x, y, n):
        '''
        Create a circle to represent a state.

        @param x -- int, x position
        @param y -- int, y position
        @param n -- int, state number
        '''
        self.canvas.create_oval(x-self.state_rad, y-self.state_rad, 
                                x+self.state_rad, y+self.state_rad,
                                outline='black', fill='white', tags='state')
        self.canvas.create_oval(x-self.state_rad+5, y-self.state_rad+5, 
                                x+self.state_rad-5, y+self.state_rad-5,
                                outline='black', fill='white', tags='state')
        self.canvas.create_text(x, y, text='s{}'.format(n), tags='text')

    def create_line(self, xA, yA, xB, yB, label='', pos='left'):
        '''
        Join two states with a directional line.
        Input state centre position.

        @param xA -- int, State A x pos
        @param yA -- int, State A y pos
        @param xB -- int, State B x pos
        @param yB -- int, State B y pos
        @param label -- str
        @param pos -- str, options = ['left', 'top', 'bottom'], defaults to left
        '''
        posX = 0
        posY = 0

        if pos is 'top':
            posY = -self.state_rad
        elif pos is 'bottom':
            posY = self.state_rad
        else:
            posX = -self.state_rad

        self.canvas.create_line((xA, yA), (xB + posX, yB + posY), smooth=True, arrow=tk.LAST, tags='link')

        textX = xA + ( (xB-xA) / 2 ) - 5
        textY = yA - ( (yA-yB) / 2 ) - 10
        self.canvas.create_text(textX, textY, text=label, tags='text')

    def create_arc_line(self, xA, yA, xB, yB, d, direction='forward', label='', r=40):
        '''
        Join two states with a curved directional line.

        @param xA -- int, State A x pos
        @param yA -- int, State A y pos
        @param xB -- int, State B x pos
        @param yB -- int, State B y pos
        @param direction -- str
        @param label -- str, options = ['back', 'forward']
        @param d -- int
        '''
        if direction is 'back':
            # curve backward under
            posY = -self.state_rad
            xC = xA + (xB-xA)/2
            yC = yA - r * d
            textY = yC + (yA-yC)/2 - 15
        else:
            # curve forward over
            posY = self.state_rad
            xC = xA + (xB-xA)/2
            yC = yA + r * d / 2
            textY = yC - (yC-yA)/2 - 5

        self.canvas.create_line((xA, yA), (xC, yC), (xB, yB+posY), smooth=True, arrow=tk.LAST)
        self.canvas.create_text(xC, textY, text=label, tags='text')


def create_nfa(app, nfa):
    '''
    Create a series of circles and lines to represent the given NFA.

    @param nfa -- NFA
    @param app -- tk.Tk
    '''
    # state pos and state tuples in list
    state_pos = {}
    
    app.ratio = int(app.screenwidth / 13)
    x = app.ratio
    y = app.screenheight / 2

    state_pos[0] = (x, y)

    for state, links in iter(nfa):
        # 0, 1 or 2 out links
        x, y = state_pos[state.state_no]

        if x + app.ratio >= app.screenwidth:
            for i in state_pos:
                xv, yv = state_pos[i]
                state_pos[i] = (xv*.75, yv)
                app.ratio *= .75

        if links:
            # first state link
            s1, c1 = links[0]
            # current states x, y position

            if len(links) == 2:
                # second state link
                s2, c2 = links[1]
                if s1.state_no in state_pos:
                    #
                    if s2.state_no in state_pos:
                        x1, y1 = state_pos[s2.state_no]
                        state_pos[s2.state_no] = (x+app.ratio, y1-app.ratio/2)
                    else:
                        state_pos[s2.state_no] = (x+app.ratio, y)
                else:
                    state_pos[s1.state_no] = (x+app.ratio, y-app.ratio/2)
                    state_pos[s2.state_no] = (x+app.ratio, y+app.ratio/2)
            else:
                if s1.state_no in state_pos:
                    x1, y1 = state_pos[s1.state_no]
                    if x < x1:
                        x = x1
                    else:
                        x = x+app.ratio
                    state_pos[s1.state_no] = (x, y1+app.ratio/2)
                else:
                    state_pos[s1.state_no] = (x+app.ratio, y)

    draw_nfa(app, nfa, state_pos)

def draw_nfa(app, nfa, state_pos):
    for state, links in iter(nfa):
        n = state.state_no
        x, y = state_pos[n]
        if n == 0:
            app.create_line(40, y, x, y)
        if links:
            for s, c in links:
                x1, y1 = state_pos[s.state_no]
                if s.state_no < n:
                    app.create_arc_line(x, y, x1, y1, n - s.state_no, direction='back', label=c)
                elif y == y1 and s.state_no-1 > n:
                    app.create_arc_line(x, y, x1, y1, s.state_no - n, direction='forward', label=c)
                else:
                    if x1 - x > 2 * app.ratio and y1 < y:
                        app.create_arc_line(x, y, x1, y1, s.state_no - n, direction='forward', label=c)
                    else:
                        app.create_line(x, y, x1, y1, label=c)
            app.create_state(x, y, n)
        else:
            app.create_final_state(x, y, n)


if __name__ == '__main__':
    app = RegexApp()
    app.mainloop()
