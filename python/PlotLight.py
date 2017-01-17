from tkinter import *
import math
import time

class PlotLight():
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
			self.canvas.delete('temp-light') # delete items tagged as temp-light

		x1 = self.x2
		y1 = self.y2
		self.x2 = 930 - self.s * 8
		self.y2 = (((self.unit.getLight() * -1) / 200) * 50) + 300
		self.canvas.create_line(x1, y1, self.x2, self.y2, fill='red', tags='temp-light')
		self.s = self.s + 1

	def keepPlotting(self):
		self.plotOneStep()
		self.canvasCommand = self.canvas.after(self.pauseInMs, self.keepPlotting)