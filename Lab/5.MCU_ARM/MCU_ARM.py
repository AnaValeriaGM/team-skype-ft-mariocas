import RPi.GPIO as GPIO
import time
import smbus

#Set warnings of the default input pins to False.
GPIO.setwarnings(False)

#Specify which way the IO pins on a Raspberry Pi within RPI.GPIO are numbered.
GPIO.setmode(GPIO.BOARD)

#Setup every channel used as Input or Output.
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)

#Create a SMBus instance.
bus = smbus.SMBus(1)
#Address that the i2c device will read from.
DEVICE_ADDRESS = 0x48
print('  Starting.../n')

#Create a loop that functions as an LM3194 with two input voltages connected to the ADC device.
while True:
    #Create a reference voltage variable in address 0x00.
    Vref = bus.read_byte_data(DEVICE_ADDRESS, 0x00)
    #Create an input voltage variable in address 0x01.
    Vin = bus.read_byte_data(DEVICE_ADDRESS, 0x01)
    #Create a switch variable in address 0x02 to change how the output will be displayed, dot or bar.
    #Bar: switch = 0, Dot: switch = 1.
    switch = bus.read_byte_data(DEVICE_ADDRESS, 0x02)
    print('Vref = ', Vref, 'Vin = ', Vin, 'Sw = ', switch)
    #Create a variable for the 8 LEDs in total
    eight = Vref/8
    time.sleep(.5)
    #Every LED needs to be declared as on(1) or off(0).
    #Bar display
    if switch > 0:
        if Vin >= Vref:
            GPIO.output(29, 1)
            GPIO.output(31, 1)
            GPIO.output(33, 1)
            GPIO.output(35, 1)
            GPIO.output(37, 1)
            GPIO.output(32, 1)
            GPIO.output(36, 1)
            GPIO.output(38, 1)
        else:
            if Vin <= eight:
                GPIO.output(29, 1)
                GPIO.output(31, 0)
                GPIO.output(33, 0)
                GPIO.output(35, 0)
                GPIO.output(37, 0)
                GPIO.output(32, 0)
                GPIO.output(36, 0)
                GPIO.output(38, 0)
            elif Vin <= eight*2:
                GPIO.output(29, 1)
                GPIO.output(31, 1)
                GPIO.output(33, 0)
                GPIO.output(35, 0)
                GPIO.output(37, 0)
                GPIO.output(32, 0)
                GPIO.output(36, 0)
                GPIO.output(38, 0)
            elif Vin <= eight*3:
                GPIO.output(29, 1)
                GPIO.output(31, 1)
                GPIO.output(33, 1)
                GPIO.output(35, 0)
                GPIO.output(37, 0)
                GPIO.output(32, 0)
                GPIO.output(36, 0)
                GPIO.output(38, 0)
            elif Vin <= eight*4:
                GPIO.output(29, 1)
                GPIO.output(31, 1)
                GPIO.output(33, 1)
                GPIO.output(35, 1)
                GPIO.output(37, 0)
                GPIO.output(32, 0)
                GPIO.output(36, 0)
                GPIO.output(38, 0)
            elif Vin <= eight*5:
                GPIO.output(29, 1)
                GPIO.output(31, 1)
                GPIO.output(33, 1)
                GPIO.output(35, 1)
                GPIO.output(37, 1)
                GPIO.output(32, 0)
                GPIO.output(36, 0)
                GPIO.output(38, 0)
            elif Vin <= eight*6:
                GPIO.output(29, 1)
                GPIO.output(31, 1)
                GPIO.output(33, 1)
                GPIO.output(35, 1)
                GPIO.output(37, 1)
                GPIO.output(32, 1)
                GPIO.output(36, 0)
                GPIO.output(38, 0)
            elif Vin <= eight*7:
                GPIO.output(29, 1)
                GPIO.output(31, 1)
                GPIO.output(33, 1)
                GPIO.output(35, 1)
                GPIO.output(37, 1)
                GPIO.output(32, 1)
                GPIO.output(36, 1)
                GPIO.output(38, 0)
            elif Vin <= eight*8:
                GPIO.output(29, 1)
                GPIO.output(31, 1)
                GPIO.output(33, 1)
                GPIO.output(35, 1)
                GPIO.output(37, 1)
                GPIO.output(32, 1)
                GPIO.output(36, 1)
                GPIO.output(38, 1)
    #Dot display
    else:
        if Vin >= Vref:
            GPIO.output(29, 0)
            GPIO.output(31, 0)
            GPIO.output(33, 0)
            GPIO.output(35, 0)
            GPIO.output(37, 0)
            GPIO.output(32, 0)
            GPIO.output(36, 0)
            GPIO.output(38, 1)
        else:
            if Vin <= eight:
                GPIO.output(29, 1)
                GPIO.output(31, 0)
                GPIO.output(33, 0)
                GPIO.output(35, 0)
                GPIO.output(37, 0)
                GPIO.output(32, 0)
                GPIO.output(36, 0)
                GPIO.output(38, 0)
            elif Vin <= eight*2:
                GPIO.output(29, 0)
                GPIO.output(31, 1)
                GPIO.output(33, 0)
                GPIO.output(35, 0)
                GPIO.output(37, 0)
                GPIO.output(32, 0)
                GPIO.output(36, 0)
                GPIO.output(38, 0)
            elif Vin <= eight*3:
                GPIO.output(29, 0)
                GPIO.output(31, 0)
                GPIO.output(33, 1)
                GPIO.output(35, 0)
                GPIO.output(37, 0)
                GPIO.output(32, 0)
                GPIO.output(36, 0)
                GPIO.output(38, 0)
            elif Vin <= eight*4:
                GPIO.output(29, 0)
                GPIO.output(31, 0)
                GPIO.output(33, 0)
                GPIO.output(35, 1)
                GPIO.output(37, 0)
                GPIO.output(32, 0)
                GPIO.output(36, 0)
                GPIO.output(38, 0)
            elif Vin <= eight*5:
                GPIO.output(29, 0)
                GPIO.output(31, 0)
                GPIO.output(33, 0)
                GPIO.output(35, 0)
                GPIO.output(37, 1)
                GPIO.output(32, 0)
                GPIO.output(36, 0)
                GPIO.output(38, 0)
            elif Vin <= eight*6:
                GPIO.output(29, 0)
                GPIO.output(31, 0)
                GPIO.output(33, 0)
                GPIO.output(35, 0)
                GPIO.output(37, 0)
                GPIO.output(32, 1)
                GPIO.output(36, 0)
                GPIO.output(38, 0)
            elif Vin <= eight*7:
                GPIO.output(29, 0)
                GPIO.output(31, 0)
                GPIO.output(33, 0)
                GPIO.output(35, 0)
                GPIO.output(37, 0)
                GPIO.output(32, 0)
                GPIO.output(36, 1)
                GPIO.output(38, 0)
            elif Vin <= eight*8:
                GPIO.output(29, 0)
                GPIO.output(31, 0)
                GPIO.output(33, 0)
                GPIO.output(35, 0)
                GPIO.output(37, 0)
                GPIO.output(32, 0)
                GPIO.output(36, 0)
                GPIO.output(38, 1)
