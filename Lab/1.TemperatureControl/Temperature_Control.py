#Import libraries
import RPi.GPIO as GPIO
import time
import smbus
from RPLCD.gpio import CharLCD

#Specify which way the IO pins on a Raspberry Pi within RPI.GPIO are numbered.
GPIO.setmode(GPIO.BOARD)

#Define GPIO pins to LCD mapping.
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33,31,29,23], numbering_mode=GPIO.BOARD)
lcd.write_string(u"Starting...")

#Set variable for pin.
Motor = 12

#Setup channel used as Input or Output.
GPIO.setup(Motor,GPIO.OUT)

#Frequency used in the Pulse Width Modulation (PWM) of the motor.
fq = 50

#Create a PWM instance for the motor.
M1 = GPIO.PWM(12, fq)

#Create a SMBus instance.
bus = smbus.SMBus(1)

#Address that the ADC(Analog to Digital Converter) device will read from, via protocol i2c.
DEVICE_ADDRESS = 0x48
print('starting...\n')

#Create a method based in Fuzzy Logic to measure the sensor temperature.
def Read(Input):
    Vref = 5
    AnlogIn = (Vref*Input)/((2**8) -1) *100
    x = AnlogIn
    print('\n', Input)
    a = 20
    b = 25
    c = 30
    d = 50
    z = 0
    l1 = 0
    l2 = 0
    l3 = 0
    l4 = 0
    mayor = 0
    menor = 0
    L = ""
    R = 0
    R2 = 0
    rpm = 500

    if x <= a and x > 0:
        R = 1
        R2 = 0
        print(x, "Cold")
        return x
        L = "cold"
    if x > a and x < b:
        R = (b - x)/(b - a)
        R2 = (x - a)/(b - a)
        print(x, "Warm-Cold")
        return x
    if x > b and x < c:
        R = (x - b)/(c - b)
        R2 = (c - x)/(c - b)
        print(x, "Warm-Hot")
        return x
    if x >= c and x <= d:
        R = 1
        R2 = 0
        print(x, "Hot")
        return x
        L = "hot"
    if x == b:
        R = 0
        R2 = 1
        print(x, "Warm")
        return x
    if R > R2 and x > a and x < b:
        print(x + R, "More Cold than Warm")
        res = x + R
        return res
    if R > R2 and x > b and x < c:
        print(x + R, "More Hot than Warm")
        res = x + R
        return res
    if R2 > R and x != b:
        L = "warm"
        res = x + R2
        return res
        print(x + R2, "More Warm than anything else")

    if R > R2:
        mayor = R
        menor = R2
    else:
        mayor = R2
        menor = R

    if L == "cold":
        l1 = 0
        l2 = 25
        l3 = 0
        l4 = 0
    elif L == "warm" and x < 25:
        l1 = 0
        l2 = (50-25)*(mayor)+25
        l3 = -(75-50)*(mayor)+75
        l4 = -(75-50)*(menor)+75
    elif L == "warm" and x > 25:
        l1 = (50-25)*(mayor)+25
        l2 = -(75-50)*(mayor)+75
        l3 = (75-50)*(menor)+50
        l4 = 100
    elif L == "hot":
        l1 = 0
        l2 = 0
        l3 = 75
        l4 = 100

    pwm = mayor*((l1+l2)/2)+ menor*((l3+l4)/2)
    print(pwm)

#Create a temporal variable used when a change in the temperature exists.
temporal = 0

#Create a loop that reads from the ADC device, interprets and sends the temperature to the LCD and motor if it is different from the temporal variable.
while True:
    #Reads from the ADC device in address 0x00 (where the sensor is connected to).
    x = bus.read_byte_data(DEVICE_ADDRESS, 0x00)
    time.sleep(1)
    if temporal!= x:
        temporal = x
        pwm = Read(x)
        #Starts PWM
        M1.start(pwm + 20)
        #Writes in LCD the Temperature.
        lcd.clear()
        lcd.cursor_pos=(0,0)
        lcd.write_string(u"Temp: " + str(pwm) + "C")
        lcd.cursor_pos=(1,0)
        lcd.write_string(u"TeamSkype")
    else:
        pass
