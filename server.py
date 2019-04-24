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
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCP_Socket:
		TLS_Socket = ssl.wrap_socket(TCP_Socket, certfile="./cert/cert.pem", server_side=True, ssl_version=ssl.PROTOCOL_TLS)
		TLS_Socket.bind(('', int(port)))
		TLS_Socket.listen(5)
		print("Server listening on port + " + str(port))

def runOneThree(port):
	return(2)

main()
