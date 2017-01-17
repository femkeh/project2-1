from tkinter import *
from PlotTemp import *
from PlotLight import *
import time

class View():
	def __init__(self, canvas, unit):
		self.canvas = canvas
		self.unit = unit
		
		###--- drawGraph ---###

		self.canvas.create_line(450,300,930,300, width=2) # x-axis
		self.canvas.create_line(450,300,450,50, width=2) # y-axis lichtintensiteit
		self.canvas.create_line(930,300,930,50, width=2) # y2-axis temperatuur
		self.canvas.create_line(0,450,1000,450, width=2) # bottom GUI

		# x-axis
		for i in range(7):
			x = 450 + (i * 80) #offset vanaf linker scherm rand = 450 + voor elke stap ix80 verderop een lijn
			self.canvas.create_line(x,300,x,50, width=1, dash=(2,5)) 
			self.canvas.create_text(x,300, text='%d'% (10*(i-6)), anchor=N) 
		self.canvas.create_text(x-50,320, text='Time in seconds', font = "Helvetica 16 bold", anchor=N) 

		# y-axis lux
		for i in range(6):
			y = 300 - (i * 50)
			self.canvas.create_line(450,y,930,y, width=1, dash=(2,5))
			if (i == 0):
				self.canvas.create_text(440,y, text='0', anchor=E)
			else: 
				self.canvas.create_text(440,y, text='%d00'% (i*2), anchor=E)
		self.canvas.create_text(440,35, text='Lichtintensiteit', font = "Helvetica 16 bold", anchor=E, fill='red')

		# y-axis temp (-40, 60)
		for i in range(6):
			y = 300 - (i * 50) #offset vanaf linker scherm rand = 50 + voor elke stap ix50 verderop een lijn
			self.canvas.create_text(960,y, text='%d'% (20*(i-2)), anchor=E)
		self.canvas.create_text(990,35, text='Degrees Celsius', font = "Helvetica 16 bold", anchor=E, fill='blue')


		###---- drawLinesInGraph ----####
		s = 1
		x2 = 930
		yTemp = (((self.unit.getTemp() * -1) / 20) * 50) + 200
		yLight = (((self.unit.getLight() * -1) / 200) * 50) + 300

		# Update de lijnen van temperatuur en lichtintensiteit
		plotTemp = PlotTemp(s, x2, yTemp, 1000, self.unit, self.canvas)
		plotLight = PlotLight(s, x2, yLight, 1000, self.unit, self.canvas)
		plotTemp.keepPlotting()
		plotLight.keepPlotting()




