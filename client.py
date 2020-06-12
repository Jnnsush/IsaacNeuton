from __future__ import print_function, absolute_import

from pynput.keyboard import Key, Listener, KeyCode
import socket
import sys

from protocol import send_key_action, ACTION_PRESS, ACTION_RELEASE

LISTEN_KEYS = [
	Key.up, 
	Key.down, 
	Key.left, 
	Key.right, 
	Key.enter,
	KeyCode.from_char('w'),
	KeyCode.from_char('a'),
	KeyCode.from_char('s'),
	KeyCode.from_char('d'),
]

client_socket = None

class Client(object):
	def __init__(self):
		client_socket = None
		self.pressed_keys = []

	def connect(self, ip, port):
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client_socket.connect((ip, port))
		print("Connected!!!")

	def on_press(self, key):
		if key in LISTEN_KEYS and key not in self.pressed_keys:
			self.pressed_keys.append(key)
			send_key_action(self.client_socket, key, ACTION_PRESS)
			print("Pressed {}".format(key))

	def on_release(self, key):
		if key in LISTEN_KEYS and key in self.pressed_keys:
			send_key_action(self.client_socket, key, ACTION_RELEASE)
			self.pressed_keys.remove(key)
			print("Released {}".format(key))

	def run_clinet(self, ip, port):
		self.connect(ip, port)
		with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
			listener.join()


if __name__ == "__main__":
	client = Client()
	client.run_clinet(sys.argv[1], int(sys.argv[2]))
