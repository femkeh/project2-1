import time
import serial as s
from Communication.Protocol import *

ser = s.Serial('/dev/tty.usbmodem621', 19200)
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

# for i in range(0, 50):
# getTemperature
# Met light: 23, 24, gebruik read_double
ser.write([42])
ser.write([1])
ser.write([54])
byte = read_byte()
if (byte < 20 and byte > 10):
    print("Light limit is set") # print("Temp limit set on:", read_byte())   read_temp(read_byte())
else:
    print("some kind of error:", protocol.get(byte).title) #.get('title'))
ser.write([24])
byte = read_byte()
if (byte < 20 and byte > 10):
    print("Light limit is set on:", read_double()) # print("Temp limit set on:", read_byte())   read_temp(read_byte())
else:
    print("some kind of error:", protocol.get(byte).title) #.get('title'))
# print(read_temp((tempTotal / tempReads)))
    # time.sleep(0.05)

ser.close()
