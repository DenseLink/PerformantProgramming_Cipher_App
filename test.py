import curses
from curses.textpad import Textbox, rectangle

screen = curses.initscr() #This initializes the curses by determining the terminal type
curses.noecho() #This enables the program to read keys and only display them under certain circumstances
curses.cbreak() #This allows the program to react instantly without requiring the Enter key to be pressed

screen.addstr(0, 0, "Enter message, then press Ctrl-G:")
rows, cols = 25, 80
window = curses.newwin(5, 30, 2, 1) # h, w, y, x
rectangle(screen, 1, 0, 7, 32)      # win, y1, x1, y2, x2
screen.refresh()                    # Draw to the screen

box = Textbox(window)               # Create a textbox
box.edit()                          # Enable editing

curses.endwin()                     # End curses mode
print("Message:\n%s" % box.gather())

