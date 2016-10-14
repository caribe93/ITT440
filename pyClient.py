import socket

host = 'localhost'
port = 80
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
s.send('welcome python socket')
data = s.recv(size)
s.close()
print 'Received:', data 
