# Project: Client-Server TLS Analysis
# Programmer: Jacob Grubb
# Organization: Southern Illinois University Edwardsville, CS 490, Spring 2019
# Due Date: 04/29/2019 23:59:59
# File: server.py

import socket
import sys
import os
import datetime
import ssl
import _thread

def main():
	if(len(sys.argv) != 3):
		print("Syntax Error:\npython3 server.py <server-port> <operation_mode>")
		print("Operation Modes: \n'TLS1.3' = TLS 1.2\n'TLS1.3' = TLS 1.3")
		exit(1)
	os.system("clear")
	mode = sys.argv[2]
	port = sys.argv[1]
	if(mode == "TLS1.2"):
		runOneTwo(port)
	elif(mode == "TLS1.3"):
		runOneThree(port)
	else:
		print("Syntax Error:\npython3 ./server.py <server-port> <operation_mode>")
		print("Operation Modes: \n'TLS1.2' = TLS 1.2\n'TLS1.3' = TLS 1.3")
		exit(1)
	
def runOneTwo(port):
	ssl.OP_NO_TLSv1_3 = True
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCP_Socket:
		TLS_Socket = ssl.wrap_socket(TCP_Socket, certfile="./cert/cert.pem", server_side=True, ssl_version=ssl.PROTOCOL_TLSv1_2)
		TLS_Socket.bind(('', int(port)))
		TLS_Socket.listen(5)
		print("Server listening on port + " + str(port))
		while True:
			try:
				(Incoming_Socket, address) = TLS_Socket.accept()
				_thread.start_new_thread(handleConnection, (Incoming_Socket, address))
			except(ssl.SSLError):
				print("Connection rejected")

def runOneThree(port):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCP_Socket:
		TLS_Socket = ssl.wrap_socket(TCP_Socket, certfile="./cert/cert.pem", server_side=True, ssl_version=ssl.PROTOCOL_TLS)
		TLS_Socket.bind(('', int(port)))
		TLS_Socket.listen(5)
		print("Server listening on port + " + str(port))
		while True:
			try:
				(Incoming_Socket, address) = TLS_Socket.accept()
				_thread.start_new_thread(handleConnection, (Incoming_Socket, address))
			except(ssl.SSLError):
				print("Connection rejected")

def handleConnection(Incoming_Socket, address):
	print(str(datetime.datetime.now()) + " " + str(address) + " Connected")
	try:
		while(True):
			message = Incoming_Socket.recv(4096)
			if(message == b''):
				Incoming_Socket.close()
				print(str(address) + " closed by client")
				return
			print(str(address) + " says: " + str(message)[2:-1])
			Incoming_Socket.send(str.encode("Got msg at: " + str(datetime.datetime.now())))
	except(ConnectionResetError):
		print(str(address) + " closed by client")
main()
