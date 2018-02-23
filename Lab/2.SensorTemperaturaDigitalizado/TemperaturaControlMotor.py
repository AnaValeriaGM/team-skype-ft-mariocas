import RPi.GPIO as GPIO
import time
import sys
import smbus
from RPLCD.gpio import CharLCD

GPIO.setmode(GPIO.BOARD)
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33,31,29,23], numbering_mode=GPIO.BOARD)
lcd.write_string(u"Starting...")
Motor1A = 12

GPIO.setup(Motor1A,GPIO.OUT)

fq = 50

M1A = GPIO.PWM(12, fq)

bus = smbus.SMBus(1)
DEVICE_ADDRESS = 0x48
print('starting...\n')

##while True:
##    x = bus.read_byte(DEVICE_ADDRESS)
##    print (x)
##    time.sleep(1)
 
def Read(Input):
    Vref = 5
    AnlogIn = (Vref*Input)/((2**8) -1) *100
##    x = float(input("ingrese la temperatura"  ))
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
    R = 0 # grado de membresia de los trapecios
    R2 = 0 # grado  de membresia del triangulo
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
        # l1,l2 = "cold","warm"
    if R > R2 and x > b and x < c:
        print(x + R, "More Hot than Warm")
        res = x + R
        return res
        # l1,l2 = "warm","hot"
    if R2 > R and x != b:
        L = "warm"
        # if x < b:
            # l1,l2 = "warm","hot"
        # else:
            # l1,l2 = "cold","warm"
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

y = 0
while True:
    x = bus.read_byte_data(DEVICE_ADDRESS, 0x00)
    time.sleep(1)
    if y!= x:
        lcd.clear()
        y = x
        pwm = Read(x)
        M1A.start(pwm + 20)
        lcd.cursor_pos=(0,0)
        lcd.write_string(u"Temp: " + str(pwm) + "C")
        lcd.cursor_pos=(1,0)
        lcd.write_string(u"TeamSkype")
    else:
        pass 
