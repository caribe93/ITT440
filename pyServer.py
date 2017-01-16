import socket
import RPi.GPIO as GPIO
import time

ledPin = 23 #Red LED position
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.output(ledPin, GPIO.LOW)

host = '127.0.0.1'
port = 80
backlog = 5
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)

print("\n\nServer is now ready to receive data from Client side. Press CTRL+C to exit")
try:
        while 1:
 		client, address = s.accept()
                data = client.recv(size)
                if data:
                        client.send(data)
                        GPIO.output(ledPin, GPIO.HIGH)
                        time.sleep(2.0)
                        GPIO.output(ledPin, GPIO.LOW)
                        time.sleep(2.0)
			GPIO.output(ledPin, GPIO.HIGH)
                        time.sleep(2.0)
                        GPIO.output(ledPin, GPIO.LOW)
                        time.sleep(2.0)

                client.close()
                print("Red LED blinks two times indicating Data is sucessfully sent back from Server to Client")
except KeyboardInterrupt:
                        GPIO.cleanup()

