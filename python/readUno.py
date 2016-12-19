import time
import serial as s

ser = s.Serial('/dev/ttyACM0', 19200)
time.sleep(2)

# read one byte and use ord to make it an int
def read_byte():
    byte = ord(ser.read(1))
    return byte

def read_double():
    byte = (ord(ser.read(1)) << 8)
    byte += ord(ser.read(1))
    return byte

def read_temp(byteIn):
    temp = 0.0
    temp = byteIn * (5000.0/1024)
    temp = ((temp - 500) / 10)
    return temp

tempReads = 0
tempTotal = 0

for i in range(0, 50):
    if (read_byte() == 255):
        print("Lightlevel:", (read_double()))
    if (read_byte() == 254):
        print("Temp:", read_temp(read_byte()))
    # print("byte:", read_byte())
    # tempTotal += read_byte()
    # tempReads += 1
    # print("tempRead: " + str(tempRead))
    # tempTotal += tempRead
    # tempReads += 1
    # tempRead = read_temp(rawDbl)
# print(read_temp((tempTotal / tempReads)))
    # time.sleep(0.05)

ser.close()
