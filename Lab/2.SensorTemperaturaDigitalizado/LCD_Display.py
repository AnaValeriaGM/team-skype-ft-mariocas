import RPi.GPIO as GPIO
import time
from RPLCD import CharLCD

#Establishes the LCD parameters and the pins that are going to be used, in this case 33, 31, 29, 23
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33,31,29,23],numbering_mode=GPIO.BOARD)
GPIO.setwarnings(False)

#Initialization of the LCD
while True:
    lcd.clear()
    lcd.write_string("LCD is working")
    time.sleep(5)
