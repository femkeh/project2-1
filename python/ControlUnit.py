import serial
import time

class ControlUnit:
	def __init__(self, ser, protocol):
		self.ser = ser
		self.protocol = protocol

	# def getCommand(self, commandId):
	# 	command = self.protocol[commandId]

	# 	self.ser.write([commandId])

	# 	responseId = self.read_byte()
	# 	if (responseId < 11 or responseId > 20):
	# 		return False

	# 	response = self.protocol[responseId]
	# 	i = response['getMoreData']
	# 	data = 0
	# 	while (i):
	# 		data += (self.read_byte() << 8 * i)
	# 		i -= 1;

	def getCommand(self, commandId):
		self.ser.write([commandId])

		responseId = self.read_byte()
		if (responseId < 11 or responseId > 20):
			return False

		data = 0
		if (responseId == 12):
			data = self.read_byte()

		if (responseId == 13):
			data = self.read_double()


		return data


	def getTemp(self):
		self.ser.write([21])

		responseId = self.read_byte()
		if (responseId < 11 or responseId > 20):
			return False

		data = self.read_temp(self.read_byte())

		return data

	def getLight(self):
		self.ser.write([23])

		responseId = self.read_byte()
		if (responseId < 11 or responseId > 20):
			return False

		data = self.read_double()

		return data


	def getTempLimit(self):
		self.ser.write([22])

		responseId = self.read_byte()
		if (responseId < 11 or responseId > 20):
			return False

		data = self.read_temp(self.read_byte())

		return data


	def getLightLimit(self):
		self.ser.write([24])

		responseId = self.read_byte()
		if (responseId < 11 or responseId > 20):
			return False

		data = self.read_double()

		return data


	def setCommand(self, commandId, value):
		self.ser.write([commandId])
		self.ser.write([int(value)])
		responseId = self.read_byte()
		if (responseId < 11 or responseId > 20):
			return False


	def setTempLimit(self, value):
		self.ser.write([41])
		self.ser.write([int(self.reverse_read_temp(int(value)))])
		responseId = self.read_byte()
		if (responseId < 11 or responseId > 20):
			return False


	def setLightLimit(self, value):
		value1 = 0
		value2 = 0
		if (int(value) - 256) < 0:
			value1 = 0
			value2 = int(value)
		else:
			value1 = 1
			value2 = int(value) - 256

		self.ser.write([42])
		self.ser.write([value1])
		self.ser.write([value2])
		responseId = self.read_byte()
		if (responseId < 11 or responseId > 20):
			return False

	def setRolldownLimit(self, value):
		value1 = 0
		value2 = 0
		if (int(value) - 256) < 0:
			value1 = 0
			value2 = int(value)
		else:
			value1 = 1
			value2 = int(value) - 256

		self.ser.write([43])
		self.ser.write([value1])
		self.ser.write([value2])
		responseId = self.read_byte()
		if (responseId < 11 or responseId > 20):
			return False

	def read_byte(self):
		byte = ord(self.ser.read(1))
		return byte

	def read_double(self):
	    byte = (ord(self.ser.read(1)) << 8)
	    byte += ord(self.ser.read(1))
	    return byte

	def read_temp(self, byteIn):
	    temp = 0.0
	    temp = byteIn * (5000.0/1024)
	    temp = ((temp - 500) / 10)
	    return temp

	def reverse_read_temp(self, value):
	    value = value * 10 + 500
	    value = value / (5000.0/1024)
	    return value
