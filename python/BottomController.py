from tkinter import *
from tkinter import messagebox

class BottomController():
	def __init__(self, canvas):
		self.canvas = canvas		

		###--- drawButtonsBottom ---###

		# Waardes van de verschillende limits
		self.lightLimitValue = 0
		self.temperatureLimitValue = 0
		self.windowHeightValue = 0

		# Light limit
			#Entry
		self.lightEntry = Entry(self.canvas, width=7) #textvariable=self.light_limit
		self.lightEntry_window = self.canvas.create_window(130, 400, window=self.lightEntry) 
		self.lightEntry.insert(10, "0")
			#Save button
		self.buttonLightSave = Button(self.canvas, text="Save", command=self.setLimitLight)
		self.buttonLightSave_window = self.canvas.create_window(192, 400, window=self.buttonLightSave)
			#Label
		self.labelLight = Label(self.canvas, text="Light limit:")
		self.labelLight_window = self.canvas.create_window(60, 400, window=self.labelLight) 
			#Output
		self.textLight = Label(self.canvas, text=self.lightLimitValue)     
		self.textLight_window = self.canvas.create_window(112, 428, window=self.textLight)

		# Temperature limit
			#Entry
		self.temperatureEntry = Entry(self.canvas, width=7) #textvariable=self.temperature_limit
		self.temperatureEntry_window = self.canvas.create_window(475, 400, window=self.temperatureEntry)
		self.temperatureEntry.insert(10, "0") 
			#Save button
		self.buttonTempSave = Button(self.canvas, text="Save", command=self.setLimitTemp)
		self.buttonTempSave_window = self.canvas.create_window(537, 400, window=self.buttonTempSave)
			#Label
		self.labelTemp = Label(self.canvas, text="Temperature limit:")
		self.labelTemp_window = self.canvas.create_window(380, 400, window=self.labelTemp)
			#Output
		self.textTemp = Label(self.canvas, text=self.temperatureLimitValue)     
		self.textTemp_window = self.canvas.create_window(457, 428, window=self.textTemp)

		# Window limit
			#Entry 
		self.windowEntry = Entry(self.canvas, width=7) #textvariable=self.window_hight
		self.windowEntry_window = self.canvas.create_window(791, 400, window=self.windowEntry) 
		self.windowEntry.insert(10, "0")
			#Save button
		self.buttonWindow = Button(self.canvas, text="Save", command=self.setLimitWindow)
		self.buttonWindow_window = self.canvas.create_window(853, 400, window=self.buttonWindow)
			#Label
		self.labelWindow = Label(self.canvas, text="Window height:")
		self.labelWindow_window = self.canvas.create_window(705, 400, window=self.labelWindow) 
			#Output
		self.textWindow = Label(self.canvas, text=self.temperatureLimitValue)     
		self.textWindow_window = self.canvas.create_window(773, 428, window=self.textWindow)

		# General
		self.canvas.create_text(58,420, text='Current value:', font = "Helvetica 10 bold", anchor=N)

	def setLimitLight(self):
		if len(self.lightEntry.get()) > 0 and int(self.lightEntry.get()) > 0 and int(self.lightEntry.get()) < 100000:
		
			self.lightLimitValue = int(self.lightEntry.get())
			try:
				self.lightLimitValue = self.lightEntry.get()
				self.lightEntry.delete(0,END)
				self.textLight.destroy()
				self.textLight = Label(self.canvas, text=self.lightLimitValue)     
				self.textLight_window = self.canvas.create_window(112, 428, window=self.textLight)
			
			except ValueError:
				pass
		else: 
			messagebox.showwarning("INVALID ENTRY!","This is not a valid entry, please try again.")
	def setLimitTemp(self):
		if len(self.temperatureEntry.get()) > 0 and int(self.temperatureEntry.get()) > -40 and int(self.temperatureEntry.get()) < 59 : # meer ifs
			self.temperatureLimitValue = int(self.temperatureEntry.get())
			try:
				self.temperatureLimitValue = self.temperatureEntry.get()
				self.temperatureEntry.delete(0,END)
				self.textTemp.destroy()
				self.textTemp = Label(self.canvas, text=self.temperatureLimitValue)     
				self.textTemp_window = self.canvas.create_window(457, 428, window=self.textTemp)
			
			except ValueError:
				pass
		else:
			messagebox.showwarning("INVALID ENTRY!", "This is not a valid entry, please try again. The minimum temperature is -40°c and the maximum is 58°c.")
	def setLimitWindow(self):
		if len(self.windowEntry.get()) > 0 and int(self.windowEntry.get()) > 0.5 and int(self.windowEntry.get()) < 440: # meer ifs
			self.temperatureLimitValue = int(self.windowEntry.get())
			try:
				self.windowLimitValue = self.windowEntry.get()
				self.windowEntry.delete(0,END)
				self.textWindow.destroy()
				self.textWindow = Label(self.canvas, text=self.windowLimitValue)     
				self.textWindow_window = self.canvas.create_window(773, 428, window=self.textWindow)
			
			except ValueError:
				pass
		else:
			messagebox.showwarning("INVALID ENTRY!", "This is not a valid entry, please try again. The minimum height is 0.5cm and the maximum height is 440 cm.")