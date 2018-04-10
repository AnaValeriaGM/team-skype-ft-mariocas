import RPi.GPIO as GPIO
import time
import smbus

#Specifies which way the IO pins on a Raspberry Pi within RPI.GPIO are numbered.
GPIO.setmode(GPIO.BOARD)

#Set variables for pins of Motors 1 and 2.
Motor1 = 22
Motor2 = 21

#Setups every channel used as Input or Output
GPIO.setup(Motor1,GPIO.OUT)
GPIO.setup(Motor2,GPIO.OUT)

#Frequency used by the Pulse Width Modulation (PWM) of both motors.
fq = 50

#Creates a PWM instance for Motors 1 and 2.
M1 = GPIO.PWM(22, fq)
M2 = GPIO.PWM(21, fq)

#Create a SMBus instance.
bus = smbus.SMBus(1)
#Address that our i2c device will read from.
DEVICE_ADDRESS = 0x48
print('starting...\n')

#Method that scales our input into a range of variables (from 0.0 to 100.0) for PWM.
def Read(Input):
    x = float(Input)
    x = x/25.6
    print('\nInput = ', Input,'	PWM = ',x) 
    return x

#Loop that reads from our i2c device, which the joystick is connected to, and using our method 'Read()' sends a scaled signal to our motors.
while True:
    #Only the axis x (address 0x00) and y (address 0x01) where used from the joystick.
    x = bus.read_byte_data(DEVICE_ADDRESS, 0x00)
    y = bus.read_byte_data(DEVICE_ADDRESS, 0x01)
    time.sleep(.1)
    x = Read(x)
    y = Read(y)
    #Starts PWM and changes the Duty Cycle.
    M1.start(5)
    M1.ChangeDutyCycle(x)
    M2.start(5)
    M2.ChangeDutyCycle(y) 
