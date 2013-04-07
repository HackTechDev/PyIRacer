import sys
import select
import tty
import termios
import bluetooth
import time
from evdev import InputDevice, categorize, ecodes
 
if __name__ == '__main__':
 
 
	bd_addr = "00:12:05:09:98:43"
	port = 1
	sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	sock.connect((bd_addr, port))

	# 0x5X for left forward. 0x51 very slow. 0x5F fastest
	sock.send('\x5A')
	time.sleep(3);
	# 0x6X for right forward. 0x11 very slow. 0x1F fastest
	sock.send('\x6A')
	time.sleep(3);
	# 0x2X for straight backward. 0x21 very slow. 0x2F fastest
	sock.send('\x2A')
	time.sleep(3);
	# 0x1X for straight forward. 0x11 very slow. 0x1F fastest
	sock.send('\x1A')
	time.sleep(3);
	#stop
	sock.send('\x00')
