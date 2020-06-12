from __future__ import print_function, absolute_import

from pynput.keyboard import Key, Controller
import socket
import sys

from protocol import receive_key_action, ACTION_PRESS, ACTION_RELEASE

class Server(object):
	def __init__(self, ip , port):
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.bind((ip, port))
		self.server_socket.listen(1)
		self.client_socket = None
		self.keyboard = Controller()

	def accept(self):
		self.client_socket, client_addr = self.server_socket.accept()
		print("Client connected from address {}!".format(client_addr))

	def serve_forever(self):
		try:
			while True:
				self.press_remote_key()
		except socket.error:
			print("Connection closed!")

	def press_remote_key(self):
		key, action = receive_key_action(self.client_socket)
		if key is None:
			return
		if action == ACTION_PRESS:
			self.keyboard.press(key)
			print("Pressed {}".format(key))
		elif action == ACTION_RELEASE:
			self.keyboard.release(key)
			print("Released {}".format(key))


if __name__ == '__main__':
	server = Server(sys.argv[1], int(sys.argv[2]))
	server.accept()
	server.serve_forever()
	print("Server Done!")
