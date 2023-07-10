ESC = '\033['
OSC = '\033]'
BEL = '\007'
SEP = ';'

cursorLeft = ESC + 'G'
cursorSavePosition = ESC + 's'
cursorRestorePosition = ESC + 'u'
cursorGetPosition = ESC + '6n'
cursorNextLine = ESC + 'E'
cursorPrevLine = ESC + 'F'
cursorHide = ESC + '?25l'
cursorShow = ESC + '?25h'

eraseEndLine = ESC + 'K'
eraseStartLine = ESC + '1K'
eraseLine = ESC + '2K'
eraseDown = ESC + 'J'
eraseUp = ESC + '1J'
eraseScreen = ESC + '2J'
scrollUp = ESC + 'S'
scrollDown = ESC + 'T'

def clear(a=0):
    """ Function to clear the screen

    Args:
        area (int, optional): The screen area to clear. Defaults to 0.
                                0 clears from cursor until end of screen.
                                1 clears from cursor to beginning of screen.
                                2 clears entire screen.
    """
    print(f'{ESC}{a}J', end='', flush=True)

def clear_line():
    print(f'{ESC}K', end='', flush=True)

def move_up(n=1):
    """ Function to move the cursor up

    Args:
        n (int, optional): Number of lines to move the cursor up. Defaults to 1.
    """
    print(f'{ESC}{n}A', end='', flush=True)

def move_down(n=1):
    """ Function to move the cursor down

    Args:
        n (int, optional): Number of lines to move the cursor down. Defaults to 1.
    """
    print(f'{ESC}{n}B', end='', flush=True)
    
def move_forward(n=1):
    """ Function to move the cursor forward (right)

    Args:
        n (int, optional): Number of spaces to move the cursor right. Defaults to 1.
    """
    print(f'{ESC}{n}C', end='', flush=True)

def move_backward(n=1):
    """ Function to move the cursor backward (left)

    Args:
        n (int, optional): Number of spaces to move the cursor left. Defaults to 1.
    """
    print(f'{ESC}{n}D', end='', flush=True)
    
def save_position():
    """ Function to save the cursor position
    
    Note. Generating new terminal space by printing newlines when the cursor is at the 
    bottom of the page, the saved cursor position will shift by the number of newlines generated.
    """
    print(f'{ESC}s', end='', flush=True)

def restore_position():
    """ Function to retore the saved cursor position
    """
    print(f'{ESC}u', end='', flush=True)

def bold_text():
    """ Function to set the text format to  bold
    """
    print(f'{ESC}1m', end='', flush=True)

def dim_text():
    """ Function to set the text format to dim
    """
    print(f'{ESC}2m', end='', flush=True)

def italic_text():
    """ Function to set the text format to italic
    """
    print(f'{ESC}3m', end='', flush=True)

def underline_text():
    """ Function to set the text format to underline
    """
    print(f'{ESC}4m', end='', flush=True)

def invert_colours():
    """ Function to invert the terminal colours
    """
    print(f'{ESC}7m', end='', flush=True)

def hide_text():
    """ Function to hide the text
    """
    print(f'{ESC}8m', end='', flush=True)

colours = {'bl': 0,
           'r': 1,
           'g': 2,
           'y': 3,
           'b': 4,
           'm': 5,
           'c': 6,
           'w': 7,
           'black': 0,
           'red': 1,
           'green': 2,
           'yellow': 3,
           'blue': 4,
           'magenta': 5,
           'cyan': 6,
           'white': 7,
           40: 0,
           41: 1,
           42: 2,
           43: 3,
           44: 4,
           45: 5,
           46: 6,
           47: 7,
           30: 0,
           31: 1,
           32: 2,
           33: 3,
           34: 4,
           35: 5,
           36: 6,
           37: 7}    

def set_text_colour(c):
    """ Function to set the text colour
    """
    print(f'{ESC}{30+colours[c]}m', end='', flush=True)
    
def set_background_colour(c):
    """ Function to set the background colour
    """
    print(f'{ESC}{40+colours[c]}m', end='', flush=True)
    
def reset():
    """ Function to reset all text attributes and formatting to default
    """
    print(f'{ESC}0m', end='', flush=True)
    
# TODO: Create a print/dump class that can be used to print mapping/indexable object in a static possition in the terminal.
# class StaticDump:
#     def __init__(self, template, *args, **kwargs):
#         super().__init__(*args, **kwargs)
        
#         self.coord = dict()
#         self.dump(template)
#         print(self.coord)
                        
#     def dump(self, obj, nested_level=0, i_prev=0):
#         spacing = 4
#         if isinstance(obj, dict):
#             for i, (k, v) in enumerate(obj.items()):
#                 if hasattr(v, '__iter__'):
#                     print(f'{(nested_level)*spacing}{k}:')
#                     self.dump(v, nested_level + 1)
#                 else:
#                     print(f'{(nested_level)*spacing}{k}: {v}')
#         elif isinstance(obj, list):
#             # print(f'{(nested_level)*spacing}[')
#             for i, v in enumerate(obj):
#                 key = nested_level + i + i_prev
#                 if hasattr(v, '__iter__'):
#                     self.dump(v, nested_level, i + i_prev)
#                 else:
#                     self.coord.update({key:((nested_level + 1)*spacing, key)})
#             print(f'{(nested_level)*spacing}]')
#         else:
#             print(f'{(nested_level)*spacing}{obj}')