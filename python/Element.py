from tkinter import *
from View import *
from SideController import *
from BottomController import *

class Element:
	def __init__(self, parentframe, naam, ser, s):
		self.elementCanvas=Canvas(parentframe, width=1000, height=450) # border om element?
		self.elementCanvas.pack()
		self.naam = naam
		self.ser=ser
		self.s=s

		View(self.elementCanvas)
		SideController(self.elementCanvas, self.naam, self.ser, self.s)
		BottomController(self.elementCanvas)
