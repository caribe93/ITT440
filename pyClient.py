import socket

host = 'localhost'
port = 80
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((host,port))
s.send("Welcome to SOCKET PYTHON Programming. Shhh... This is between us only !\n\n")
data = s.recv(size)
s.close()

print'SECRET MESSAGE CLIENT SEND TO SERVER THEN SENDS BACK FROM SERVER TO CLIENT  :\n\n', data 
