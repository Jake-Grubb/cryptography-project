# Project: Client-Server TLS Analysis
# Programmer: Jacob Grubb
# Organization: Southern Illinois University Edwardsville, CS 490, Spring 2019
# Due Date: 04/29/2019 23:59:59
# File: client.py

import socket
import sys
import os
import datetime
import ssl


def main():
	if(len(sys.argv) != 4):
                print("Syntax Error:\npython3 client.py <server-host> <server-port> <operation-mode>")
                print("Operation Modes: \n'TLS1.2' = TLS 1.2\n'TLS1.3' = TLS 1.3\n'Degraded' = degrade")
                exit(1)
	server_ip = sys.argv[1]
	server_port = sys.argv[2]
	op_mode = sys.argv[3]

	if(op_mode == "TLS1.2"):
		runOneTwo(server_ip, server_port)
	elif(op_mode == "TLS1.3"):
		runOneThree(server_ip, server_port)
	elif(op_mode == "degrade"):
		runDegrade(server_ip, server_port)
	else:
		print("Syntax Error:\npython3 client.py <server-host> <server-port> <operation-mode>")
		print("Operation Modes: \n'TLS1.2' = TLS 1.2\n'TLS1.3' = TLS 1.3")
		exit(1)

def runOneTwo(server_ip, server_port):
	ssl.OP_NO_TLSv1_3 = True
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCP_Socket:
		TLS_Socket = ssl.wrap_socket(TCP_Socket, server_side=False, ssl_version=ssl.PROTOCOL_TLSv1_2)
		TLS_Socket.connect((server_ip, int(server_port)))
		os.system("clear")
		print("Now connected to " + server_ip + ":" + str(server_port) + "\n")
		while(True):
			userInput = input(">")
			if(userInput == "quit" or userInput == "exit"):
				TLS_Socket.close()
				print("Connection closed")
				return
			TLS_Socket.send(str.encode(userInput))
			response = TLS_Socket.recv(2048)
			print("Server sent back: " + str(response)[2:-1])

def runOneThree(server_ip, server_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCP_Socket:
                TLS_Socket = ssl.wrap_socket(TCP_Socket, server_side=False, ssl_version=ssl.PROTOCOL_TLS)
                TLS_Socket.connect((server_ip, int(server_port)))
                os.system("clear")
                print("Now connected to " + server_ip + ":" + str(server_port) + "\n")
                while(True):
                        userInput = input(">")
                        if(userInput == "quit" or userInput == "exit"):
                                TLS_Socket.close()
                                print("Connection closed")
                                return
                        TLS_Socket.send(str.encode(userInput))
                        response = TLS_Socket.recv(2048)
                        print("Server sent back: " + str(response)[2:-1])

def runDegrade(server_ip, server_port):
	ssl.OP_NO_TLSv1_2 = True
	ssl.OP_NO_TLSv1_1 = True
	ssl.OP_NO_TLSv1 = True
	ssl.OP_NO_SSLv3 = False
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCP_Socket:
		TLS_Socket = ssl.wrap_socket(TCP_Socket, server_side=False, ssl_version=ssl.PROTOCOL_TLSv1)
		TLS_Socket.connect((server_ip, int(server_port)))
		os.system("clear")
		print("Now connected to " + server_ip + ":" + str(server_port) + "\n")
		while(True):
			userInput = input(">")
			if(userInput == "quit" or userInput == "exit"):
				TLS_Socket.close()
				print("Connection closed")
				return
			TLS_Socket.send(str.encode(userInput))
			response = TLS_Socket.recv(2048)
			print("Server sent back: " + str(response)[2:-1])

main()
