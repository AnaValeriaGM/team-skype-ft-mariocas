import smbus
import time

#Create a SMBus instance.
bus = smbus.SMBus(1)
#Address that the i2c device will read from.
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
        L = "cold"
    if x > a and x < b:
        R = (b - x)/(b - a)
        R2 = (x - a)/(b - a)
        print("Warm-Cold")
    if x > b and x < c:
        R = (x - b)/(c - b)
        R2 = (c - x)/(c - b)
        print("Warm-Hot")
    if x >= c and x <= d:
        R = 1
        R2 = 0
        print(x, "Hot")
        L = "hot"
    if x == b:
        R = 0
        R2 = 1
        print(x, "Warm")
    if R > R2 and x > a and x < b:
        print(x + R, "More Cold than Warm")
    if R > R2 and x > b and x < c:
        print(x + R, "More Hot than Warm")
    if R2 > R and x != b:
        L = "warm"
        print(x + R2, "More Warm than anything else")

    print("1 = Metodo de peso promedio")
    if R > R2:
        mayor = R
        menor = R2
    else:
        mayor = R2
        menor = R
    print("R , R2",R," ",R2)

    if L == "cold":
        print ("im in ")
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
    print(l1,l2,l3,l4)
    print(pwm)
    
#Create a temporal variable used when a change in the temperature exists.
temporal = 0

#Create a loop that reads from the i2c device, interprets and prints the temperature if it is different from the temporal variable.
while True:
    #Reads from the i2c device in address 0x00 (where the sensor is connected to).
    x = bus.read_byte_data(DEVICE_ADDRESS, 0x00)
    time.sleep(1)
    if temporal!= x:
        temporal = x
        Read(x)
    else:
        pass 
