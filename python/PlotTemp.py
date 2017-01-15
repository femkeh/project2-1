from tkinter import *
import math
import time

class PlotTemp():
	_PLOT_STEP_BOUNDARY = 61

	def __init__(self, s, x2, y2, pauseInMs, unit, canvas):
		self._plottingPaused = False
		self.s = s
		self.x2 = x2
		self.y2 = y2
		self.pauseInMs = pauseInMs
		self.yMinValue = 0
		self.yMaxValue = 100
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
		if self.s == self._PLOT_STEP_BOUNDARY:
			# step limit reached; draw a new plot
			self.s = 1
			self.x2 = 930
			self.canvas.delete('temp-temp') # only delete items tagged as temp-temp

		x1 = self.x2
		y1 = self.y2
		self.x2 = 930 - self.s * 8
		self.y2 = (((self.unit.getTemp() * -1) / 20) * 50) + 200
		self.canvas.create_line(x1, y1, self.x2, self.y2, fill='blue', tags='temp-temp')
		self.s = self.s + 1

	def keepPlotting(self):
		self.plotOneStep()
		self.canvasCmdAfterId = self.canvas.after(self.pauseInMs, self.keepPlotting)