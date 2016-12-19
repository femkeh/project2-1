from tkinter import *

class View():
	def __init__(self, canvas):
		self.canvas = canvas
		
		###--- drawGraph ---###

		self.canvas.create_line(450,300,930,300, width=2) # x-axis
		self.canvas.create_line(450,300,450,50, width=2) # y-axis lux
		self.canvas.create_line(930,300,930,50, width=2) # y2-axis temperatuur
		self.canvas.create_line(0,450,1000,450, width=2) # bottom GUI

		# x-axis
		for i in range(7):
			x = 450 + (i * 80) #offset vanaf linker scherm rand = 50 + voor elke stap ix100 verderop een lijn
			self.canvas.create_line(x,300,x,50, width=1, dash=(2,5)) 
			self.canvas.create_text(x,300, text='%d'% (10*(i-6)), anchor=N) 
		self.canvas.create_text(x-50,320, text='Time in minutes', font = "Helvetica 16 bold", anchor=N) 

		# y-axis lux
		for i in range(6):
			y = 300 - (i * 50)
			self.canvas.create_line(450,y,930,y, width=1, dash=(2,5))
			if (i == 0):
				self.canvas.create_text(440,y, text='0', anchor=E)
			else: 
				self.canvas.create_text(440,y, text='%d.000'% (20*i), anchor=E)
		self.canvas.create_text(440,35, text='Lux', font = "Helvetica 16 bold", anchor=E)

		# y-axis temp (-40, 60)
		for i in range(6):
			y = 300 - (i * 50) #offset vanaf linker scherm rand = 50 + voor elke stap ix100 verderop een lijn
			self.canvas.create_text(960,y, text='%d'% (20*(i-2)), anchor=E)
		self.canvas.create_text(990,35, text='Degrees Celsius', font = "Helvetica 16 bold", anchor=E)