import curses
import curses.textpad

ciphertexts = []
needed_lines = 0
key_text = ""
temp_key = ""
crib = ""
crib_pos = 1
which_cipher = 0

def display_window():
    line = 0
    y,x = stdscr.getmaxyx()
    if crib == "":
        stdscr.addstr(y-1,0,"H-help\tQ-quit\tC-type cipher\tK-type key\tB-type crib", curses.A_STANDOUT)
    else:
        s = "H-help\tQ-quit\tC-type cipher\tK-type key\tB-type crib"
        t = "F-move left\tG-move right\tNext Cipher\tPrevious Cipher\tA-accept key"
        stdscr.addstr(y-2,0,s, curses.A_STANDOUT)
        stdscr.addstr(y-1,0,t, curses.A_STANDOUT)
    stdscr.addstr(line, 0, "One-Time Pad Cracking Tool\n", curses.A_BOLD)

    pad = stdscr.subpad(2,0)
    for cipher in ciphertexts:
        y,x = pad.getyx()
        pad.addstr(y+1, 0, "Ciphertext", curses.A_BOLD)
        y,x = pad.getyx()
        pad.addstr(y+1, 0, cipher)
        y,x = pad.getyx()
        pad.addstr(y+1, 0, "Plaintext", curses.A_BOLD)
        y,x = pad.getyx()
        if temp_key != "":
            pad.addstr(y+1, 0, deciper(cipher, temp_key))
        else:
            pad.addstr(y+1, 0, deciper(cipher, key_text))
        y,x = pad.getyx()
        line = y+1
    if temp_key != "":
        pad.addstr(line+1, 0, "Test Key", curses.A_BOLD)
        y,x = pad.getyx()
        pad.addstr(y+1,0,temp_key)
    elif key_text != "":
        pad.addstr(line+1, 0, "Key", curses.A_BOLD)
        y,x = pad.getyx()
        pad.addstr(y+1,0,key_text)

def deciper(cipher, k):
    decrypt = ""
    for i in range(len(cipher)):
        d = chr(((ord(cipher[i]) - ord(k[i])) % 26) + ord('a'))
        decrypt += d
    return decrypt

def create_temp_key_chunk(cipher, plain):
    chunk = ""
    for i in range(len(cipher)):
        c = chr(((ord(cipher[i]) - ord(plain[i])) % 26) + ord('a'))
        chunk += c
    return chunk

def get_some_text():
    stdscr.erase()
    tb = curses.textpad.Textbox(stdscr, insert_mode=True)
    text = tb.edit()
    return ''.join([i for i in text if i.isalpha()])

def adjust_temp_key():
    global crib_pos
    global crib
    global temp_key
    global ciphertexts
    global which_cipher
    if crib != "":
        c = ciphertexts[which_cipher]
        offset = len(c)-len(crib)-crib_pos
        temp_key = key_text[:offset]
        temp_key += create_temp_key_chunk(c[(-len(crib)-crib_pos):-crib_pos],crib)
        temp_key += key_text[len(c)-crib_pos:]

def pad_key():
    global key_text
    if len(ciphertexts) != 0:
        padlen = len(max(ciphertexts, key=len)) - len(key_text)
        pad_string = "A" * padlen
        key_text += pad_string

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)
stdscr.scrollok(True)
stdscr.refresh()
while 1:
    stdscr.erase()
    display_window()
    c = stdscr.getch()
    if c == ord('q'):
        break
    elif c == ord('c'):
        ciphertexts.append(get_some_text().upper())
        pad_key()
    elif c == ord('k'):
        key_text = get_some_text().upper()
        pad_key()
    elif c == ord('b'):
        crib = get_some_text()
        adjust_temp_key()
    elif c == ord('h'):
        with open("help.txt") as f:
            content = f.read()
            stdscr.erase()
            stdscr.addstr(content)
            stdscr.getkey()
    elif c == ord('f'):
        crib_pos += 1
        if crib_pos >= len(temp_key):
          crib_pos = len(temp_key)-1
        adjust_temp_key()
    elif c == ord('g'):
        crib_pos -= 1
        if crib_pos <= 0:
          crib_pos = 1
        adjust_temp_key()
    elif c == ord('1'):
        which_cipher -= 1
        if (which_cipher < 0):
          which_cipher = len(ciphertexts) - 1
        crib_pos = 1
        adjust_temp_key()
    elif c == ord('2'):
        which_cipher += 1
        if (which_cipher >= len(ciphertexts)):
          which_cipher = 0
        crib_pos = 1
        adjust_temp_key()
    elif c == ord('a'):
        if temp_key != "":
            key_text = temp_key
            crib = ""
            crib_pos = 1

curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
