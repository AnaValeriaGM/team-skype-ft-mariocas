import RPi.GPIO as GPIO
import time
import smbus

GPIO.setmode(GPIO.BOARD)

Motor1A = 22
Motor2A = 21

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor2A,GPIO.OUT)

fq = 50

M1A = GPIO.PWM(22, fq)
M2A = GPIO.PWM(21, fq)

bus = smbus.SMBus(1)
DEVICE_ADDRESS = 0x48
print('starting...\n')
 
def Read(Input):
    x = float(Input)
    x = x/25.6
    print('\nInput = ', Input,'	PWM = ',x) 
    return x

while True:
    x = bus.read_byte_data(DEVICE_ADDRESS, 0x00)
    y = bus.read_byte_data(DEVICE_ADDRESS, 0x01)
    time.sleep(.1)
    x = Read(x)
    y = Read(y)
    M1A.start(5)
    M1A.ChangeDutyCycle(x)
    M2A.start(5)
    M2A.ChangeDutyCycle(y) 
