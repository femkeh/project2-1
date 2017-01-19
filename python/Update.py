from tkinter import *
import math
import time

class Update():

	def __init__(self, s, pauseInMs, unit, canvas):
		self._plottingPaused = False
		self.pauseInMs = pauseInMs
		self.yMinValue = 0
		self.yMaxValue = 100
		self.s = s
		self.unit = unit
		self.canvas = canvas

	def togglePlotting(self):
		# current state = paused
		if self._plottingPaused: 
			self.keepPlotting()
			self._plottingPaused = False
		# current state = running
		else: 
			self.canvas.after_cancel(self.canvasCommand) # cancel queued command
			self._plottingPaused = True

	def plotOneStep(self):
		while (self.unit.getCommand(29)):
			blink = True

		self.canvas.delete('temp-status') # delete items tagged as temp-status

		status = ""
		statusValue = self.unit.getCommand(27) #"Rolled down" 
		if statusValue == 0:
			status = "Rolled down"
		else:
			status = "Rolled up     "
		self.canvas.create_text(90,25, text='Status: %s'% status, font = "Helvetica 14 bold", anchor=N, tag='temp-status')

		temp = str(round(self.unit.getTemp())) + " °C"
		self.canvas.create_text(170,120, text=' %s'% temp, font = "Helvetica 95 bold", anchor=N, tag='temp-status')

	def keepPlotting(self):
		self.plotOneStep()
		self.canvasCommand = self.canvas.after(self.pauseInMs, self.keepPlotting)