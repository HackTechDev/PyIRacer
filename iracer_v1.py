# 
# Interface de controle iRacer
#

import sys
import select
import tty
import termios
import bluetooth
import time
from evdev import InputDevice, categorize, ecodes
from Tkinter import *

sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )

def eventInfo(eventName, char, keysym, ctrl, shift):
    msg = "[" + char + "] " 
    if char == "z":
        msg += "Avancer Droit"
	sock.send('\x1A')
	time.sleep(0.5);
	sock.send('\x00')
    elif char == "s":
        msg += "Reculer Droit"
	sock.send('\x2A')
	time.sleep(0.5);
	sock.send('\x00')
    elif char == "q":
        msg += "Avancer Gauche"
	sock.send('\x5A')
        time.sleep(0.5);
        sock.send('\x00')
	sock.send('\x3A')
    elif char == "d":
        msg += "Avancer Droite"
	sock.send('\x6A')
        time.sleep(0.5);
        sock.send('\x00')
	sock.send('\x4A')
    elif char == "w":
        msg += "Reculer Gauche"
	sock.send('\x7A')
        time.sleep(0.5);
        sock.send('\x00')
	sock.send('\x3A')
    elif char == "c":
        msg += "Reculer Droite"
	sock.send('\x8A')
        time.sleep(0.5);
        sock.send('\x00')
	sock.send('\x4A')

    elif char == "a":
        msg += "Arreter"
	sock.send('\x00')
    else:
	msg += "Inconnu"	

    return msg

def ignoreKey(event):
    ignoreSyms = [ "Shift_L", "Shift_R", "Control_L", "Control_R", "Caps_Lock" ]
    return (event.keysym in ignoreSyms)
    
def keyPressed(event):
    canvas = event.widget.canvas
    ctrl  = ((event.state & 0x0004) != 0)
    shift = ((event.state & 0x0001) != 0)
    if (ignoreKey(event) == False):
        canvas.data["info"] = eventInfo("keyPressed", event.char, event.keysym, ctrl, shift)
    if ((len(event.keysym) == 1) and (event.keysym.isalpha())):
        if (event.keysym not in canvas.data["pressedLetters"]):
            canvas.data["pressedLetters"].append(event.keysym)
    redrawAll(canvas)    


def redrawAll(canvas):
    canvas.delete(ALL)
    font = ("Arial", 16, "bold")
    info = canvas.data["info"]
    canvas.create_text(400, 50, text=info, font=font)

def init(canvas):
    canvas.data["info"] = "Mouvement"
    canvas.data["pressedLetters"] = [ ]
    redrawAll(canvas)

def run():

    bd_addr = "00:12:05:09:98:43"
    port = 1
    sock.connect((bd_addr, port))
    
    root = Tk()
    root.title("Controleur iRacer")
    canvas = Canvas(root, width=800, height=200)
    canvas.pack()
    root.canvas = canvas.canvas = canvas
    canvas.data = { }
    init(canvas)
    root.bind("<KeyPress>", keyPressed)
    root.mainloop()

run()
