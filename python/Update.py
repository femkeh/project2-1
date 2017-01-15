from tkinter import *
import math
import time

class Update():
	# _PLOT_STEP_BOUNDARY = 10

	def __init__(self, s, pauseInMs, unit, canvas):
		self._plottingPaused = False
		self.pauseInMs = pauseInMs
		self.yMinValue = 0
		self.yMaxValue = 100
		self.s = s
		self.unit = unit
		self.canvas = canvas

	def togglePlotting(self):
		if self._plottingPaused: # current state is paused
			self.keepPlotting()
			self._plottingPaused = False
		else: # current state is running
			self.canvas.after_cancel(self.canvasCmdAfterId) # cancel queued cmd
			self._plottingPaused = True

	def plotOneStep(self):
		# if self.s == self._PLOT_STEP_BOUNDARY:
		# 	# step limit reached; draw a new plot
		# 	self.s = 1
		self.canvas.delete('temp-status') # only delete items tagged as temp-temp

		status = ""
		statusValue = self.unit.getCommand(27) #"Rolled down" ######
		if statusValue == 0:
			status = "Rolled down"
		else:
			status = "Rolled up"
		self.canvas.create_text(85,25, text='Status: %s'% status, font = "Helvetica 10 bold", anchor=N, tag='temp-status')

		temp = str(round(self.unit.getTemp())) + " °C"
		self.canvas.create_text(170,120, text=' %s'% temp, font = "Helvetica 95 bold", anchor=N, tag='temp-status')

		# self.s = self.s + 1

	def keepPlotting(self):
		self.plotOneStep()
		self.canvasCmdAfterId = self.canvas.after(self.pauseInMs, self.keepPlotting)