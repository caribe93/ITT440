import RPi.GPIO as GPIO
import sys
sys.path.insert(0,"/home/pi/code/jarvis/MFRC522-python")
import MFRC522
import signal
import time
import socket

servoPin=7
pirPin=11
redLed=15
greenLed=13
reedSw=8

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPin,GPIO.OUT)
GPIO.setup(redLed,GPIO.OUT)
GPIO.setup(greenLed,GPIO.OUT)
GPIO.setup(pirPin,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(reedSw,GPIO.IN, pull_up_down=GPIO.PUD_UP)

pwm=GPIO.PWM(servoPin,50)
pwm.start(11.4)
GPIO.output(redLed,GPIO.HIGH)
GPIO.output(greenLed,GPIO.LOW)
continue_reading=True

UDP_IP = "192.168.201.2"
UDP_PORT = 5005

print ("\nCLIENT CONFIGURATION DETAILS.")
print "IP: ",UDP_IP
print "Port: ",UDP_PORT
print "\nSERVER ONLINE.\n"

#PIR sensor output
def motionSensor(ev=None):
    	if GPIO.input(pirPin):     # True = Rising
        	global counter
        	counter += 1
        	print('INTRUDER ALERT !! TOTAL:{0}'.format(counter))
		#print("AUTOLOCK INITIATED..\n")
		#pwm.ChangeDutyCycle(11.4)
        	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        	var="WARNING !!\nINTRUDER ALERT."
        	sock.sendto(var,(UDP_IP,UDP_PORT))

#Reed switch output
def reedSwitch(ev=None):
	time.sleep(0.4)
	if GPIO.input(reedSw):
                print("FRONT DOOR OPENED !")
                GPIO.output(redLed, GPIO.LOW)
                GPIO.output(greenLed, GPIO.HIGH)
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                var="FRONT DOOR\nOPENED !"
        	sock.sendto(var,(UDP_IP,UDP_PORT))
        else:
                GPIO.output(redLed, GPIO.HIGH)
                GPIO.output(greenLed, GPIO.LOW)
                pwm.ChangeDutyCycle(11.4)
                print("FRONT DOOR CLOSED.")
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                var="FRONT DOOR\nCLOSED."
        	sock.sendto(var,(UDP_IP,UDP_PORT))
	
# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
	global continue_reading
	continue_reading = False
#	GPIO.cleanup()
#	pwm.stop()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

try:
        #PIR sensor trigger
        GPIO.add_event_detect(pirPin, GPIO.BOTH, callback=motionSensor, bouncetime=200) 
        counter = 0

        #Reed switch trigger
        GPIO.add_event_detect(reedSw, GPIO.BOTH, callback=reedSwitch, bouncetime=200)
        
	while continue_reading:
                
		# Scan for cards    
                (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    
                # Get the UID of the card
                (status,uid) = MIFAREReader.MFRC522_Anticoll()

                # If we have the UID, continue
                if status == MIFAREReader.MI_OK:

                        # Print UID
                        print "Card UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
                        card=[str(uid[0]),str(uid[1]),str(uid[2]),str(uid[3])]
                        if card == '2542220125':
                                print("WELCOME HOME HARIZ")
                        else:
                                print("WELCOME HOME BAHIJ")
                                
                        # This is the default key for authentication
                        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
                        # Select the scanned tag
                        MIFAREReader.MFRC522_SelectTag(uid)

                        # Authenticate
                        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

                        # Check if authenticated
                        if status == MIFAREReader.MI_OK:
                                pwm.ChangeDutyCycle(2.2)
                   		print("ACCESS GRANTED.")
                        	GPIO.output(greenLed,GPIO.HIGH)
                        	GPIO.output(redLed,GPIO.LOW)
                        	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                                var="ACCESS GRANTED."
                                sock.sendto(var,(UDP_IP,UDP_PORT))
				
                        else:
                            print "ACCESS DENIED."
                            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            var="ACCESS DENIED."
                            sock.sendto(var,(UDP_IP,UDP_PORT))
                
except KeyboardInterrupt:
        GPIO.cleanup()
        pwm.stop()
