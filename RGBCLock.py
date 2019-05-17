import RPi.GPIO as GPIO
import time
import serial
#import numpy

DATA_PIN = 5
CLK_PIN = 6
LATCH_PIN = 13

GPIO.setmode(GPIO.BCM)

GPIO.setup(DATA_PIN, GPIO.OUT)
GPIO.setup(CLK_PIN, GPIO.OUT)
GPIO.setup(LATCH_PIN, GPIO.OUT)

digitToInt = [63,6,91,79,102,109,125,7,127,111]
colors = [(128,128,0),(0,128,128),(220,20,60),(255,127,80),(218,165,32),(154,205,50),(50,205,50),(32,178,170),(100,149,237),(153,50,204)]
ser = serial.Serial(
        port='/dev/serial0', #Replace ttyS0 with ttyAMA0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=2
)

def shiftOut(data,dataPin,clockPin):
    #Set clock pin to LOW to prepare writing data to buffer
    GPIO.output(clockPin, GPIO.LOW)
    data = format(data,'08b')
    for i in range(len(data)): 
        #Send bit to data pin. Set it to HIGH if 1 is found, LOW otherwise
        if(data[i] == '1'): 
            GPIO.output(dataPin, GPIO.HIGH)
        else: 
            GPIO.output(dataPin, GPIO.LOW)

        #Set and reset the clock to high to accept the data
        GPIO.output(clockPin, GPIO.HIGH)
        GPIO.output(clockPin, GPIO.LOW)

counter = 0;
for dig in digitToInt:
   #Pick a color tuple and subtract from 255 as RGB pins are negative
   clr = colors[counter]
   #clrInv = numpy.subtract((255,255,255),clr)
   clrString = "R:"+str(255-clr[0])+" G:"+str(255-clr[1])+" B:"+str(255-clr[2])
   ser.write(clrString)
   ser.flush()
   #ground LATCH_PIN and hold GPIO.LOW for as long as you are transmitting
   GPIO.output(LATCH_PIN, GPIO.LOW)
   shiftOut(dig, DATA_PIN, CLK_PIN) #63 for digit 0
   #return the latch pin GPIO.HIGH to signal chip that it
   #no longer needs to listen for information
   GPIO.output(LATCH_PIN, GPIO.HIGH)
   GPIO.output(LATCH_PIN, GPIO.LOW)
   time.sleep(1) #Sleep time in seconds
   counter += 1
 