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
    # helper function to create a string with the event's info
    # also, prints the string for debug info
    msg = eventName + ": "
    msg += "(ctrl=" + str(ctrl) + ")"
    msg += "(shift=" + str(shift) + ")"
    msg += "(char=" + char + ")"
    msg += "(keysym=" + keysym + ")"
    print msg
    if char == "z":
        print "Avancer\n"
        sock.send('\x1A')
    if char == "s":
        print "Reculer\n"
        sock.send('\x2A')
    if char == "q":
        print "Gauche\n"
	sock.send('\x5A')
    if char == "d":
        print "Droite\n"
	sock.send('\x6A')
    if char == "a":
        print "Arreter\n"
	sock.send('\x00')


    return msg

def ignoreKey(event):
    # Helper function to return the key from the given event
    ignoreSyms = [ "Shift_L", "Shift_R", "Control_L", "Control_R", "Caps_Lock" ]
    return (event.keysym in ignoreSyms)
    
def keyPressed(event):
    canvas = event.widget.canvas
    ctrl  = ((event.state & 0x0004) != 0)
    shift = ((event.state & 0x0001) != 0)
    if (ignoreKey(event) == False):
        canvas.data["info"] = eventInfo("keyPressed", event.char, event.keysym, ctrl, shift)
    if ((len(event.keysym) == 1) and (event.keysym.isalpha())):
        # it's an alphabetic (A-Za-z)
        if (event.keysym not in canvas.data["pressedLetters"]):
            canvas.data["pressedLetters"].append(event.keysym)
    redrawAll(canvas)    

def keyReleased(event):
    canvas = event.widget.canvas
    ctrl  = ((event.state & 0x0004) != 0)
    shift = ((event.state & 0x0001) != 0)
    if (ignoreKey(event) == False):
        canvas.data["info"] = eventInfo("keyReleased", event.char, event.keysym, ctrl, shift)
    if ((len(event.keysym) == 1) and (event.keysym.isalpha())):
        # it's an alphabetic (A-Za-z)
        if (event.keysym in canvas.data["pressedLetters"]):
            canvas.data["pressedLetters"].remove(event.keysym)
    redrawAll(canvas)    

def redrawAll(canvas):
    canvas.delete(ALL)
    # Draw the pressedLetters
    font = ("Arial", 16, "bold")
    msg = "Pressed Letters: " + str(canvas.data["pressedLetters"])
    canvas.create_text(400, 125, text=msg, font=font)
    # Draw the event info message
    font = ("Arial", 16, "bold")
    info = canvas.data["info"]
    canvas.create_text(400, 50, text=info, font=font)

def init(canvas):
    canvas.data["info"] = "Key Events Demo"
    canvas.data["pressedLetters"] = [ ]
    redrawAll(canvas)

########### copy-paste below here ###########

def run():

    bd_addr = "00:12:05:09:98:43"
    port = 1
    sock.connect((bd_addr, port))
    
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=800, height=200)
    canvas.pack()
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    canvas.data = { }
    init(canvas)
    # set up events
    # root.bind("<Button-1>", leftMousePressed)
    root.bind("<KeyPress>", keyPressed)
    root.bind("<KeyRelease>", keyReleased)
    # timerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()
