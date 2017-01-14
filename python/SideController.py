from tkinter import *
import serial
import time

class SideController():
	def __init__(self, canvas, naam, unit, s):
		self.canvas = canvas
		self.naam = naam	
		self.unit = unit
		self.s=s

		###--- drawButtonsSide ---###
		
		#nameModule = getName()
		nameModule = self.naam
		self.canvas.create_text(52,10, text='Name: %s'% nameModule, font = "Helvetica 10 bold", anchor=N)
		#status = getStatus()
		status = ""
		statusValue = self.unit.getCommand(27) #"Rolled down" ######
		if statusValue == 0:
			status = "Rolled down"
		else:
			status = "Rolled up"
		self.canvas.create_text(85,25, text='Status: %s'% status, font = "Helvetica 10 bold", anchor=N, tag=status)
		
		temp = str(round(self.unit.getTemp())) + " °C"
		self.canvas.create_text(170,120, text=' %s'% temp, font = "Helvetica 95 bold", anchor=N)

		self.canvas.create_text(60,270, text='Manual:', anchor=N)

		self.buttonOn = Button(self.canvas, text = "On", state=NORMAL, command = self.manualOn) #Nog iets met dat die geselecteerd is, 'aan' staat
		self.buttonOn.configure(width = 7) # activebackground = "#33B5E5",
		self.buttonOn_window = self.canvas.create_window(66, 300, window=self.buttonOn) # anchor=NW,

		self.buttonOff = Button(self.canvas, text = "Off", state=DISABLED, command = self.manualOff) #anchor = SW , command = manual
		self.buttonOff.configure(width = 7) # activebackground = "#33B5E5",
		self.buttonOff_window = self.canvas.create_window(66, 325, window=self.buttonOff) # anchor=NW,

	def manualOn(self):
		self.unit.getCommand(47)

		self.buttonOn.config(state=DISABLED) 
		self.buttonOff.config(state=NORMAL) 
		self.buttonUp = Button(self.canvas, command=self.screenUp) #text = "Roll up" ''', command=self.screenUp'''
		self.photoUp = PhotoImage(file="ArrowUp.gif")
		self.buttonUp.config(image=self.photoUp,width="50",height="20")
		self.buttonUp_window = self.canvas.create_window(180, 300, window=self.buttonUp, anchor=N) 

		# self.buttonStop = Button(self.canvas, command=self.screenStop) #text = "Roll down" '', command=self.screenStop'''
		# self.photoStop = PhotoImage(file="Stop.gif")
		# self.buttonStop.config(image=self.photoStop,width="50",height="20")
		# self.buttonStop_window = self.canvas.create_window(260, 300, window=self.buttonStop, anchor=N) 
		
		self.buttonDown = Button(self.canvas, command=self.screenDown) #text = "Roll down" '', command=self.screenDown'''
		self.photoDown = PhotoImage(file="ArrowDown.gif")
		self.buttonDown.config(image=self.photoDown,width="50",height="20")
		self.buttonDown_window = self.canvas.create_window(340, 300, window=self.buttonDown, anchor=N) 

	def manualOff(self):
		self.unit.getCommand(48)

		self.buttonUp.destroy()
		self.buttonDown.destroy()
		#self.buttonStop.destroy()
		self.buttonOn.config(state=NORMAL) 
		self.buttonOff.config(state=DISABLED) 

	def screenUp(self):
		# self.s="up"
		# self.unit.write(self.s.encode('ascii'))
		# self.unit.write('\n'.encode('ascii'))
		# i=0
		# while i<3:
		# 	self.s=self.unit.readline().decode('ascii').strip()
		# 	i+=1
		# 	#print(s[0:3])
		# if self.s[0:3]=='RES': i=10
		self.unit.getCommand(50)
		# update status
		status=""
		statusValue = self.unit.getCommand(27) #"Rolled down" ######
		if statusValue == 0:
			status = "Rolled down"
		else:
			status = "Rolled up"
		self.canvas.delete("status")
		self.canvas.create_text(85,25, text='Status: %s'% status, font = "Helvetica 10 bold", anchor=N, tag="status")


	def screenDown(self):
		# self.s="down"
		# self.unit.write(self.s.encode('ascii'))
		# self.unit.write('\n'.encode('ascii'))
		# i=0
		# while i<3:
		# 	self.s=self.unit.readline().decode('ascii').strip()
		# 	i+=1
		# 	#print(s[0:3])
		# if self.s[0:3]=='RES': i=10
		self.unit.getCommand(50)
		# update status
		status=""
		statusValue = self.unit.getCommand(27) #"Rolled down" ######
		if statusValue == 0:
			status = "Rolled down"
		else:
			status = "Rolled up"
		self.canvas.delete("status")
		self.canvas.create_text(85,25, text='Status: %s'% status, font = "Helvetica 10 bold", anchor=N, tag="status")
	
	def screenStop(self):
		self.s="stop"
		self.unit.write(self.s.encode('ascii'))
		self.unit.write('\n'.encode('ascii'))
		i=0
		while i<3:
			self.s=self.unit.readline().decode('ascii').strip()
			i+=1
			#print(s[0:3])
		if self.s[0:3]=='RES': i=10
