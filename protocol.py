from pynput.keyboard import Key, KeyCode

import struct

BYTES = 64

ACTION_PRESS = 0
ACTION_RELEASE = 1

KEY_MAPPING = {
	Key.up: 0,
	Key.down: 1,  
	Key.left: 2, 
	Key.right: 3,
	Key.enter: 4,
	KeyCode.from_char('w'): 5,
	KeyCode.from_char('a'): 6,
	KeyCode.from_char('s'): 7,
	KeyCode.from_char('d'): 8,
}

REVERSE_KEY_MAPPING = [
	Key.f20,  # 0
	Key.f19,  # 1  
	Key.f18,  # 2 
	Key.f17,  # 3
	Key.f16,  # 4
	Key.f15,  # 5
	Key.f14,  # 6
	Key.f13,  # 7
	Key.f12,  # 8
]

def send_key_action(sock, key, action):
	packet = struct.pack("BB", KEY_MAPPING[key], action)
	sock.send(packet)

def receive_key_action(sock):
	try:
		packet = sock.recv(BYTES)
		mapped_key, action = struct.unpack("BB", packet)
		key = REVERSE_KEY_MAPPING[mapped_key]
		return key, action
	except struct.error:
		return None, None
