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
		# current state = paused
		if self._plottingPaused: 
			self.keepPlotting()
			self._plottingPaused = False
		# current state = running
		else: 
			self.canvas.after_cancel(self.canvasCommand) # cancel queued command
			self._plottingPaused = True

	def plotOneStep(self):
		# if step boundary reached; start from beginning of drawing plot
		if self.s == self._PLOT_STEP_BOUNDARY:
			self.s = 1
			self.x2 = 930
			self.canvas.delete('temp-temp') # delete items tagged as temp-temp, old temp line
			

		x1 = self.x2
		y1 = self.y2
		self.x2 = 930 - self.s * 8
		self.y2 = (((self.unit.getTemp() * -1) / 20) * 50) + 200
		self.canvas.create_line(x1, y1, self.x2, self.y2, fill='blue', tags='temp-temp', width=2)
		self.s = self.s + 1

		# create temp limit line
		self.canvas.delete('temp-limit') # delete items tagged as temp-temp, old temp limit line
		yTempLimit = (((self.unit.getTempLimit() * -1) / 20) * 50) + 200
		self.canvas.create_line(450,yTempLimit,930,yTempLimit, fill='blue', tags ='temp-limit') # x-axis

	def keepPlotting(self):
		self.plotOneStep()
		self.canvasCommand = self.canvas.after(self.pauseInMs, self.keepPlotting)