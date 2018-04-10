#Import libraries
import RPi.GPIO as GPIO
import time
import smbus

#Specifies which way the IO pins on a Raspberry Pi within RPI.GPIO are numbered.
GPIO.setmode(GPIO.BOARD)

#Set variables for pins of Motors 1 and 2.
Motor1 = 22
Motor2 = 21

#Setup every channel used as Input or Output
GPIO.setup(Motor1,GPIO.OUT)
GPIO.setup(Motor2,GPIO.OUT)

#Frequency used in the Pulse Width Modulation (PWM) of both motors.
fq = 50

#Create a PWM instance for Motors 1 and 2.
M1 = GPIO.PWM(22, fq)
M2 = GPIO.PWM(21, fq)

#Create a SMBus instance.
bus = smbus.SMBus(1)
#Address that the ADC(Analog to Digital Converter) device will read from, via protocol i2c.
DEVICE_ADDRESS = 0x48
print('starting...\n')

#Create a method that scales the input into PWM values (from 0.0 to 100.0).
def Read(Input):
    x = float(Input)
    x = x/25.6
    print('\nInput = ', Input,'	PWM = ',x) 
    return x

#Create a loop that reads from the ADC device all four infrared sensors, interprets and sends a scaled signal to the motors.
while True:
    #Reads all four infrared sensors.
    w = bus.read_byte_data(DEVICE_ADDRESS, 0x00)
    x = bus.read_byte_data(DEVICE_ADDRESS, 0x01)
    y = bus.read_byte_data(DEVICE_ADDRESS, 0x02)
    z = bus.read_byte_data(DEVICE_ADDRESS, 0x03)
    time.sleep(.1)
    w = Read(w)
    x = Read(x)
    y = Read(y)
    z = Read(z)
    #Axis X is made from w(left) and x(right).
    AxisX = w - x + 5
    AxisX = int(AxisX)
    print(AxisX, " Pwm")
    if AxisX >= 0 and AxisX <= 10:
        #Starts PWM and changes the Duty Cycle, in Axis X.
        M2.start(5)
        M2.ChangeDutyCycle(AxisX)
    #Axis Y is made from y(down) and z(up).
    AxisY = y - z + 5
    AxisY = int(AxisY)
    print(AxisY, " Pwm")
    if AxisY >= 0 and AxisY <= 10:
        #Starts PWM and changes the Duty Cycle, in Axis Y.
        M2.start(5)
        M2.ChangeDutyCycle(AxisY)
