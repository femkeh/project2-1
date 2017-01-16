from tkinter import *
from Element import *
from Communication.Protocol import *
from ControlUnit import *
import serial
import time

# ser = serial.Serial('/dev/ttyACM0', 19200)
# time.sleep(2)

# Main
window = Tk()
window.wm_title("Rolluiksysteem                                                                                                                             Yumthy ©")
rootcanvas = Canvas(window, borderwidth=0, width=1000, height=450)
rootframe = Frame(rootcanvas, background="#ffffff")
verticalScrollbar = Scrollbar(window, orient="vertical", command=rootcanvas.yview)
rootcanvas.configure(yscrollcommand=verticalScrollbar.set)

verticalScrollbar.pack(side="right", fill="y")
rootcanvas.pack(side="left", fill="both", expand=True)
rootcanvas.create_window(0, 0, window=rootframe, anchor=N+W)

rootframe.bind("<Configure>", lambda event, rootcanvas=rootcanvas: rootcanvas.configure(scrollregion=rootcanvas.bbox("all")))

elementen = []
connectValue =''
def insertModule():
	if len(connectEntry.get()) > 0:
		connectValue = connectEntry.get()
		ser = serial.Serial(connectValue, 19200)
		time.sleep(2)
		unit = ControlUnit(ser, protocol)
		s = 1
		number = str(len(elementen) + 1)
		name = '#%s'% number
		element = Element(rootframe, name, unit, s)
		elementen.append(element)

buttonConnection = Button(rootcanvas, text = "Connect", state=NORMAL, command = insertModule) #Nog iets met dat die geselecteerd is, 'aan' staat
buttonConnection.configure(width = 10) # activebackground = "#33B5E5",
buttonConnection_window = rootcanvas.create_window(720, 12, window=buttonConnection) # anchor=NW,
connectEntry = Entry(rootcanvas, width=7) #textvariable=self.light_limit
connectEntry_window = rootcanvas.create_window(650, 12, window=connectEntry)
connectEntry.insert(10, "COM..")


window.mainloop()
