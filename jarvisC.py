from Adafruit_CharLCD import Adafruit_CharLCD

lcd = Adafruit_CharLCD(rs=7, en=8, d4=25, d5=24, d6=23, d7=18, cols=16, lines=2)

import time
import RPi.GPIO as GPIO
import socket

lcd.message('CONNECTING....\nPLEASE WAIT')
UDP_IP ="192.168.201.2"
UDP_PORT =5005
sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_PORT))
time.sleep(2)
lcd.clear()

buzz=17   
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzz,GPIO.OUT)
GPIO.output(buzz,GPIO.LOW)

print "CLIENT ONLINE."
try:  		
        while True:
                        lcd.message(' SYSTEM ONLINE. ')
                        data, addr = sock.recvfrom(1024)
                        lcd.clear()
                        lcd.message(data)
                        GPIO.output(buzz, GPIO.HIGH)
                        time.sleep(0.5)
                        GPIO.output(buzz, GPIO.LOW)
                        print data
			time.sleep(1)
                        lcd.clear()
        
except KeyboardInterrupt:                   
    GPIO.cleanup()
    print "All cleaned up."
