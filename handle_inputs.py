import pynput
import threading
import queue

class handle_inputs():
	def __init__(self):
		self.pressed_keys = queue.Queue(8)
		self.released_keys = queue.Queue(8)
		self.list_pressed = []

	def start_thread(self):
		def on_press(key):
			if key not in self.list_pressed:
				try:
					char = key.char
				except AttributeError:
					char = key
				self.list_pressed.append(char)
				if self.pressed_keys.full() != True:
					self.pressed_keys.put_nowait(char)
		def on_release(key):
			try:
				char = key.char
			except AttributeError:
				char = key
			self.list_pressed.remove(char)
			self.released_keys.put_nowait(char)
		def start_listener():
			with pynput.keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
				listener.join()
		listener_thread = threading.Thread(target=start_listener)
		listener_thread.start()
