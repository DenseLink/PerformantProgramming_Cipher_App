import timeit
from ctypes import *
import struct
import curses
from curses import textpad
import sys
import logging
from curses.textpad import Textbox, rectangle


def cipher(message, key):
    return bytes([message[i] ^ key[i % len(key)] for i in range(0, len(message))])
def load_file():
    lib = cdll.LoadLibrary("./libxorcipher.so")
    lib.cipher.restype = None
    lib.cipher.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_int]
    return lib

def run_gui(background):
    # disable cursor blinking
    curses.curs_set(0)

    # write something on the screen
    screen = curses.initscr()  # This initializes the curses by determining the terminal type
    curses.noecho()  # This enables the program to read keys and only display them under certain circumstances
    curses.cbreak()  # This allows the program to react instantly without requiring the Enter key to be pressed

    # stdscr.addstr(0, 0, "Hello, world!")

    sh, sw = background.getmaxyx()

    #window = curses.newpad(81, 25)
    #Some variables that will be used in this while loop
    flag = True
    encoder_flag = False
    all_text = ''
    Text = "This is a haiku; it is not too long I think; but you may disagree"
    alt_Text = ''
    Key = "But there's one sound that no one knows... What does the Fox say?"
    status = "Status: Application started successfully."
    while(flag == True):
        second_window = curses.newwin(6, 25, 18, 2)
        background.addstr(1, 25, "Welcome to the XOR-Cipher App!")
        background.addstr(3, 22, "[F] Read text from a local File")
        background.addstr(4, 22, "[I] Read text from user Input prompt")
        background.addstr(5, 22, "[C] Apply C cipher to this text")
        background.addstr(6, 22, "[P] Apply Python cipher to this text")
        background.addstr(7, 22, "[V] Verify cipher results match")
        background.addstr(8, 22, "[K] Change Key used for ciphers")
        background.addstr(9, 22, "[B] Run Benchmarks on text (100000x)")
        background.addstr(10, 22, "[Q] Quit the Application")
        if (encoder_flag == False):
            if(len(Text) > 64):
                temp_text = Text[:65]
                background.addstr(13, 4, "TEXT [" + temp_text + "]")
            else:
                background.addstr(13, 4, "TEXT [" + Text + "]")
        else:
            if (len(alt_Text) > 64):
                temp_text = alt_Text[:65]
                background.addstr(13, 4, "TEXT [" + temp_text + "]")
            else:
                background.addstr(13, 4, "TEXT [" + alt_Text + "]")
        background.addstr(14, 4, "KEY  [" + Key + "]")

        third_window = curses.newpad(3, 25)
        background.addstr(24, 1, status)



        textpad.rectangle(background, 0, 0, 23, 79)  # universal box
        textpad.rectangle(background, 2, 20, 11, 59)  # Box that holds all options
        textpad.rectangle(background, 12, 2, 15, 77)  # box with haiku in it


        # update the screen
        background.refresh()
        #These are some variables used in the while loops
        c = background.getch()
        x = chr(c)
        up = str(x).upper()

        #Ensure user input is correct
        while(up.startswith("F")!=True and up.startswith("I")!=True and up.startswith("C")!=True and up.startswith("P")!=True and up.startswith("V")!=True and up.startswith("K")!=True and up.startswith("B")!=True and up.startswith("Q")!=True):
            background.addstr(17, 1, "                                                                              ")
            background.addstr(18, 1, "                                                                              ")
            background.addstr(19, 1, "                                                                              ")
            background.addstr(20, 1, "                                                                              ")
            background.addstr(21, 1, "                                                                              ")
            background.addstr(22, 1, "                                                                              ")
            background.addstr(24, 1, "                                                                 ")
            background.addstr(24, 1, "Status: ERROR: Invalid menu selection!")
            background.refresh()
            c = background.getch()
            x = chr(c)
            up = str(x).upper()
        #Load text from user input
        if(up.startswith("P") == True):
            if (encoder_flag == False):
                en = cipher(Text.encode('cp437'), Key.encode('cp437'))
            else:
                en = cipher(all_text.encode('cp437'), Key.encode('cp437'))
            all_text = en.decode('cp437')
            #Translate the characters that cannot be output under normal conditions
            ctrl_translation = str.maketrans(bytes(range(0, 32)).decode("cp437"), "�☺☻♥♦♣♠•◘○◙♂♀♪♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲▼")
            #alt_Text = all_text.translate(ctrl_translation)
            #Translate the characters that cannot be output under normal conditions
            if(encoder_flag == False):
                encoder_flag = True
                alt_Text = all_text.translate(ctrl_translation)
            else:
                encoder_flag = False
                Text = all_text.translate(ctrl_translation)
            status = "Status: Applied Python cipher."
            background.clear()
        if(up.startswith("F") == True):
            #Load Screen
            background.addstr(18, 18, "Enter file to load below, then press [ENTER]")
            textpad.rectangle(background, 17, 1, 22, 78)  # box with enter file to load
            textpad.rectangle(background, 19, 6, 21, 73)  # user interface box
            background.refresh()
            window = curses.newwin(1, 66, 20, 7)  # h, w, y, x
            box = Textbox(window)
            # Load Screen
            #Type into the Textbox created below
            file = str(box.edit()).strip()
            files = file
            # Type into the Textbox created above
            #Cancel File load if empty string is input
            if(files == ''):
                status = "Status: File load cancelled."
                background.clear()
            # Cancel File load if empty string is input
            else:
                f = open(files, mode='r')
                #all_text = f.read()
                all_text = " ".join([i.strip() for i in f])
                partial_text = 's'
                #if(len(all_text) > 64):
                #    partial_text =  all_text[:65]
                #else:
                partial_text = all_text
                Text = partial_text
                background.addstr(13, 5, "                                                                        ")
                #background.addstr(13, 5, "Text [" + partial_text + "]")
                Text = partial_text
                status = "Status: File contents loaded successfully."
                background.clear()

        if(up.startswith("I") == True):
            #Create window to write in
            background.addstr(18, 20, "Enter new text below, then press [ENTER]")
            textpad.rectangle(background, 17, 1, 22, 78)  # box with enter file to load
            textpad.rectangle(background, 19, 6, 21, 73)  # user interface box
            background.refresh()
            window = curses.newwin(1, 66, 20, 7)  # h, w, y, x
            box = Textbox(window)
            all_text = str(box.edit()).strip()
            # Create window to write in
            #Cancel File load if empty string is input
            if(all_text == ''):
                status = "Status: Cancelled user input of text (empty string)."
                background.clear()
            # Cancel File load if empty string is input
            else:
                Text = all_text
                status = "Status: New text loaded into memory from user input."
                background.clear()
        if (up.startswith("Q") == True):
            flag = False
        if (up.startswith("C") == True):
            msg = ''
            if(encoder_flag == False):
                msg = Text.encode('cp437')

            else:
                msg = all_text.encode('cp437')
            key = Key.encode('cp437')
            buf = create_string_buffer(len(msg))
            msg_len = len(msg)
            key_len = len(key)
            default = "./libxorcipher.so"
            #lib = load_file()
            lib = load_cipher_lib(default)
            lib.cipher(msg,key,buf,msg_len,key_len)
            en = buf.raw
            all_text = en.decode('cp437')
            # Translate the characters that cannot be output under normal conditions
            ctrl_translation = str.maketrans(bytes(range(0, 32)).decode("cp437"), "�☺☻♥♦♣♠•◘○◙♂♀♪♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲▼")
            # Translate the characters that cannot be output under normal conditions
            if (encoder_flag == False):
                encoder_flag = True
                alt_Text = all_text.translate(ctrl_translation)
            else:
              encoder_flag = False
              Text = all_text.translate(ctrl_translation)
              background.addstr(25, 0, Text)
              #background.refresh()
              #background.getch()
            status = "Status: Applied C cipher."
            background.clear()
        if(up.startswith("K") == True):
            background.addstr(18, 22, "Enter new key and then press [ENTER]")
            textpad.rectangle(background, 17, 1, 22, 78)  # box with enter file to load
            textpad.rectangle(background, 19, 6, 21, 73)  # user interface box
            background.refresh()
            window = curses.newwin(1, 66, 20, 7)  # h, w, y, x
            box = Textbox(window)
            all_text = str(box.edit()).strip()
            if(all_text == ''):
                status = "Status: Cancelled user input of key (empty string)."
                background.clear()
            # Cancel File load if empty string is input
            else:
                Key = all_text
                status = "Status: New key loaded into memory from user input."
                background.clear()
        if(up.startswith("V") == True):
            if (encoder_flag == False):
                p_final = cipher(Text.encode('cp437'), Key.encode('cp437'))
                p_final = p_final.decode('cp437')
                ctrl_translation = str.maketrans(bytes(range(0, 32)).decode("cp437"), "�☺☻♥♦♣♠•◘○◙♂♀♪♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲▼")
                p_final = p_final.translate(ctrl_translation)
            else:
                p_final = cipher(all_text.encode('cp437'), Key.encode('cp437'))
                p_final = p_final.decode('cp437')
                ctrl_translation = str.maketrans(bytes(range(0, 32)).decode("cp437"), "�☺☻♥♦♣♠•◘○◙♂♀♪♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲▼")
                p_final = p_final.translate(ctrl_translation)
            msg = ''
            if(encoder_flag == False):
                msg = Text.encode('cp437')
            else:
                msg = all_text.encode('cp437')
            key = Key.encode('cp437')
            buf = create_string_buffer(len(msg))
            msg_len = len(msg)
            key_len = len(key)
            #lib = load_cipher_lib()
            default = "./libxorcipher.so"
            lib = load_cipher_lib(default)
            lib.cipher(msg,key,buf,msg_len,key_len)
            en = buf.raw
            temp_text = en.decode('cp437')
            # Translate the characters that cannot be output under normal conditions
            ctrl_translation = str.maketrans(bytes(range(0, 32)).decode("cp437"), "�☺☻♥♦♣♠•◘○◙♂♀♪♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲▼")
            c_final = temp_text.translate(ctrl_translation)
            # Translate the characters that cannot be output under normal conditions

            if(c_final == p_final):
                status = "Status: Cipher match verified!"
            else:
                status = "Status: WARNING: ciphers do not match!"
            background.clear()
        if (up.startswith("B") == True):
            textpad.rectangle(background, 17, 1, 22, 78)  # box with haiku in it
            background.addstr(19, 29, "                           ")
            background.addstr(20, 29, "                           ")
            background.addstr(21, 29, "                           ")
            background.addstr(18, 29, "Running benchmarks....")
            background.refresh()
            p_text = Text
            c_text = Text
            i = 0
            p_time = timeit.timeit(lambda: (p_text.encode('cp437'), Key.encode('cp437')), number = 100000)
            msg = Text.encode('cp437')
            key = Key.encode('cp437')
            buf = create_string_buffer(len(msg))
            msg_len = len(msg)
            key_len = len(key)
            #lib = load_file()
            default = "./libxorcipher.so"
            lib = load_cipher_lib(default)
            c_time = timeit.timeit(lambda: lib.cipher(msg, key, buf, msg_len, key_len), number = 100000)
            background.clear()
            textpad.rectangle(background, 17, 1, 22, 78)  # box with haiku in it
            background.addstr(18, 29, "Results from Benchmark")
            background.addstr(19, 29, "----------------------")
            c_t = str('{:06.3f}'.format(c_time))
            p_t = str('{:06.3f}'.format(p_time))
            background.addstr(20, 29, "C-Lang Cipher: " + c_t + "s")
            background.addstr(21, 29, "Python Cipher: " + p_t + "s")
            status = "Status: Benchmark results displayed."
            background.refresh()
    # clear the screen
    background.clear()

def load_cipher_lib(library_path):
    lib = cdll.LoadLibrary(library_path)
    lib.cipher.restype = None
    lib.cipher.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_int]
    return lib

def main(stdscr):
    run_gui(stdscr)
    sys.stdout.write("Thanks for using the XOR-Cipher App; See you next time!")



curses.wrapper(main)