import smbus
import time

#Parameters for the i2c device to identify the address where it is going to read from
bus = smbus.SMBus(1)
DEVICE_ADDRESS = 0x48
print('starting...\n')

#Creates method that is based in Fuzzy Logic
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
    R = 0 # grado de membresia de los trapecios
    R2 = 0 # grado  de membresia del triangulo
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
    
#Create temporal variable if any change exists
temp = 0

#Create loop that reads from the i2c device and prints its value if it is different from the temporal variable.
while True:
    x = bus.read_byte_data(DEVICE_ADDRESS, 0x00)
    time.sleep(1)
    if temp!= x:
        temp = x
        Read(x)
    else:
        pass 
