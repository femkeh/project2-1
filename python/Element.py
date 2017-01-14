from tkinter import *
from View import *
from SideController import *
from BottomController import *

class Element:
	def __init__(self, parentframe, naam, unit, s):
		self.elementCanvas=Canvas(parentframe, width=1000, height=450) # border om element?
		self.elementCanvas.pack()
		self.naam = naam
		self.unit=unit
		self.s=s

		View(self.elementCanvas)
		SideController(self.elementCanvas, self.naam, self.unit, self.s)
		BottomController(self.elementCanvas, self.unit)
