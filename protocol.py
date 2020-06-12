from pynput.keyboard import Key, KeyCode

import struct

BYTES = 64

ACTION_PRESS = 0
ACTION_RELEASE = 1

class KeyPress(object):
	def __init__(self, press, release):
		self.press = press
		self.release = release

KEY_MAPPING = {
	Key.up: KeyPress(0, 100),
	Key.down: KeyPress(1, 101),  
	Key.left: KeyPress(2, 102), 
	Key.right: KeyPress(3, 103),
	KeyCode.from_char('w'): KeyPress(4, 104),
	KeyCode.from_char('a'): KeyPress(5, 105),
	KeyCode.from_char('s'): KeyPress(6, 106),
	KeyCode.from_char('d'): KeyPress(7, 107),
	Key.enter: KeyPress(8, 108),
}

REVERSE_KEY_MAPPING = {
	# Press
	0: Key.f1,
	1: Key.f3,
	2: Key.f5,
	3: Key.f7,
	4: Key.f9,
	5: Key.f11,
	6: Key.f13,
	7: Key.f15,
	8: Key.f17,

	# Release
	100: Key.f2,
	101: Key.f4,
	102: Key.f6,
	103: Key.f8,
	104: Key.f10,
	105: Key.f12,
	106: Key.f14,
	107: Key.f16,
	108: Key.f18,
}

def send_key_action(sock, key, action):
	if action == ACTION_PRESS:
		key_code = KEY_MAPPING[key].press
	elif action == ACTION_RELEASE:
		key_code = KEY_MAPPING[key].release
	packet = struct.pack("B", key_code)
	sock.send(packet)

def receive_key_action(sock):
	try:
		packet = sock.recv(BYTES)
		mapped_key = struct.unpack("B", packet)[0]
		key = REVERSE_KEY_MAPPING[mapped_key]
		return key
	except struct.error:
		print("Lost packet")
		return None
