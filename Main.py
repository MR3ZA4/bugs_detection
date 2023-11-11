import constants
import time
import threading
automatic = constants.automatic
bugsdetectedcam =0
bugsdetectedmic =0

#Warning - indentation may be incorrect depending on whether you open it in gedit/notepad++ or idle.
#This was written in Gedit and this can cause indentation inconsistencies in IDLE if edited, it will run fine.

def Greenarraycreator():
	"""Returns a a tuple containing: a list of centres and radii of green cockroaches in an image, a string containing non pixel text in the ppm and an array of tuples containing the RGB values of each pixel.  """
	import os
	import operator
	import constants
	filex= constants.filex
	filey = constants.filey
	maxdarknesstolerance = constants.maxdarknesstolerance
	mindarknesstolerance = constants.mindarknesstolerance
	multipledetection = constants.multipledetection
	currentx = 0
	currenty = 0
	fullarray= []
	for i in range(1,filey+1):
		fullarray.append([])
	miny = constants.miny
	minx = constants.minx
	filearray=[]
	filestring =""
	yellowled(True)
	os.system("fswebcam -d /dev/video0 -r "+str(filex)+"x"+str(filey)+" -S 4 --no-banner image.jpg")
	os.system("convert image.jpg -compress none image.ppm")
	os.system("convert image.jpg -compress none image.png")
	yellowled(False)
	file = open("image.ppm", "r")
	for i in range(0,5):
		filestring += file.readline()
		filestring += "\n"
	
	for lines in file:
		tmparray = lines.split() 
		i = 0

				
		while i< len(tmparray):
			if int(tmparray[i+1]) >= int(tmparray[i]) + 10 and int(tmparray[i+1]) >= int(tmparray[i+2]) +10:
				fullarray[currenty].append(1)


			elif int(tmparray[i]) + int(tmparray[i+1]) + int(tmparray[i+2])//3 > mindarknesstolerance and int(tmparray[i]) + int(tmparray[i+1]) + int(tmparray[i+2])//3  <= maxdarknesstolerance:
					
				fullarray[currenty].append(1)
								 
			else:
				fullarray[currenty].append(0)
					
			filearray.append((tmparray[i],tmparray[i+1],tmparray[i+2]))
					
			i += 3
			if(currentx == filex):
				currenty+=1
				currentx=1
			else:
				currentx+=1
			

						


	for y in range(0,filey-1):
		for x in range(0,filex-1):
			if fullarray[y][x] == 0:
				onecount = 0
				if fullarray[y+1][x] == 1:
					onecount+=1
				if fullarray[y][x+1] == 1:
					onecount+=1
				if y != 0:
					if fullarray[y-1][x] ==1:
						onecount+=1
				if x!= 0:
					if fullarray[y][x-1] ==1:
						onecount+=1
				if onecount == 3:
					fullarray[y][x] =1

	blob = []
	for y in range(0,filey-1):
		if sum(fullarray[y]) >= 0.25*filex:
			xcount = 0
			for x in range(0,filex-1):
				if fullarray[y][x] == 1:
					xcount+=1
				else:
					if xcount>= minx:
						ycountup = 1
						dobreak = False
						while fullarray[y+ycountup][x-(xcount//2)] != 0 and dobreak == False:
							ycountup+=1

						if ycountup+y == filey-2:

								dobreak = True
								

						if dobreak == True:
							ycountup = filey -y - 1
						dobreak = False


						ycountup -=1
						ycountdown = 1
						while fullarray[y-ycountdown][x-(xcount//2)] != 0 and dobreak == False:
							ycountdown+=1
							if ycountdown > 0:
								dobreak = True
						
						ycountdown -=1
						if ycountdown+ycountup >= miny:
							xleft = 1
							xright = 1
							while fullarray[y+((ycountup-ycountdown)//2)][(x-(xcount//2))+xleft] !=0:
								xleft += 1
							while fullarray[y+((ycountup-ycountdown)//2)][(x-(xcount//2))-xright] !=0:
								xright += 1
							if xright + xleft >= minx:
								blob.append((((x-(xcount//2))+(xleft-xright)//2,y+((ycountup-ycountdown)//2)),((xright+xleft)//2)+5,((ycountup+ycountdown)//2)+5))						

								if multipledetection == True:
									for finaly in range((y+((ycountup-ycountdown)//2)) - (((ycountup+ycountdown)//2)), (y+((ycountup-ycountdown)//2)) + (((ycountup+ycountdown)//2)+5)):
										for finalx in range(((x-(xcount//2))+(xleft-xright)//2)- (((xright+xleft)//2)), ((x-(xcount//2)-1)+(xleft-xright)//2)+ (((xright+xleft)//2))):					
											if finalx >= 0 and finaly >=0 and finalx<= filex and finaly<=filey-1:

												fullarray[finaly][finalx] = 0


								else:
									os.system("rm image.jpg")
									os.system("rm image.ppm")
									return (blob,filestring,filearray)
					xcount = 0

	
	os.system("rm image.jpg")
	os.system("rm image.ppm")
	return (blob,filestring,filearray)




def blobdetection():
	"""Uses the outputs of Greenarraycreator to check if there's a bug in the image, prints if there is, draws a red box round it and creates a ppm test file. Returns a the length of the blob array if there are bugs else False """
	import constants
	filex = constants.filex
	filey = constants.filey
	from time import strftime
	resultofpast = Greenarraycreator()
	filestring = resultofpast[1]
	filearray = resultofpast[2]
	timedetected = strftime("%Y-%m-%d %H:%M:%S")


	if len(resultofpast[0]) != 0:
		
		print("Bug detected at time: "+ timedetected)
		for val in resultofpast[0]:
			centre = val[0]
			xmax = val[1]
			ymax = val[2]


			

			for x in range(centre[0] - xmax, centre[0]+xmax):
				ytouseup =centre[1] + ymax
				ytousedown = centre[1] - ymax
				if x > 0 and x <= filex-1:
					if ytouseup <= filey-1:
						filearray[(ytouseup*filex)+x] = ("255","0","0")
				
					if ytousedown >= 0:
						filearray[(ytousedown*filex)+x] = ("255","0","0")
			
			for y in range(centre[1] - ymax, centre[1]+ymax):
				xtouseright = centre[0]+xmax
				xtouseleft = centre[0]-xmax
				if y >0 and y <=filey-1:
					if xtouseright <= filex-1:
						filearray[(y*filex)+(xtouseright)] = ("255","0","0")
					if xtouseleft >= 0:
						filearray[(y*filex)+(xtouseleft)] = ("255","0","0")


		for line in filearray:
				
			filestring+= " " + " ".join(line)
		
		ppmfile = open(timedetected +".ppm","w")
		
		ppmfile.write(filestring)
		ppmfile.close()
		return len(resultofpast[0])

		

						
				 

			
	else:
		print("No bug detected at:"+ timedetected)
		return False
		
	
def yellowled(on):
	"""Turns the yellow, green and Red LEDS on or off based on the state of the variables tracking them """
	import time
	import smbus	
	import RPi.GPIO as GPIO
	global automatic
	bus = smbus.SMBus(1)
	if on == True and automatic == True:
		bus.write_byte(0x20,0xFF)
		
	elif on == True and automatic == False:
		bus.write_byte(0x20,0xFD)
	elif on == False and automatic == True:
		bus.write_byte(0x20,0xFE)
	else:
		Reset()


	bus.close()
	


def findvoltage(I2CADDR,address):
	"""Reads value across address on device I2CADDR."""
	import smbus 
	import time  
	bus = smbus.SMBus(1) 
	bus.write_byte(I2CADDR, address) 
	tmp = bus.read_word_data(I2CADDR, 0x00) 

	if len("{0:b}".format(tmp)) > 6:
		high = tmp >> (len("{0:b}".format(tmp))-6)

		low = tmp & 0x0F

		full =int(("{0:b}".format(high)+"{0:b}".format(low)),2)
		full = float(full)
	else:
		return None
	voltage= (full/1027)*3

	bus.close()
	return voltage
	
	
def bugdetectmic():
	"""checks whether the current voltage """
	from time import strftime
	
	currentvoltage = findvoltage(0x21,0x20)
	editlights(currentvoltage)
	if currentvoltage != None:
		if currentvoltage >= L4thresh:
			print("Bug detected at time:" + strftime("%Y-%m-%d %H:%M:%S"))
			return (True)
		else:
			return (False)
			
			

def initialiselights():
	"""Initializes all the GPIO outputs for the LEDs for the software individual task  """
	import RPi.GPIO as GPIO
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	lights = [5,6,12,13,16,19,20,26]
	for light in lights:
		
		GPIO.setup(light,GPIO.OUT)
	
	#old method of setting up all the lights
	#GPIO.setup(5,GPIO.OUT)
	#GPIO.setup(6,GPIO.OUT)
	#GPIO.setup(12,GPIO.OUT)
	#GPIO.setup(13,GPIO.OUT)
	#GPIO.setup(16,GPIO.OUT)
	#GPIO.setup(19,GPIO.OUT)
	#GPIO.setup(20,GPIO.OUT)
	#GPIO.setup(26,GPIO.OUT)
	GPIO.output(5,True)

def alloff():
	"""Turns all GPIO outputs for the software individual tasks off """
	import RPi.GPIO as GPIO
	lights = [5,6,12,13,16,19,20,26]
	for light in lights:
		GPIO.output(light,False)
	
	
	#GPIO.output(5,False)
	#GPIO.output(6,False)
	#GPIO.output(12,False)
	#GPIO.output(13,False)
	#GPIO.output(16,False)
	#GPIO.output(19,False)
	#GPIO.output(20,False)
	#GPIO.output(26,False)



def editlights(voltage):
	
	"""Checks the current light level against the threshold in constants to judge what lights to turn on """
	import constants
	import RPi.GPIO as GPIO
	alloff()
	GPIO.output(5,True)
	if voltage >= constants.L1thresh:
		GPIO.output(6,True)
	if voltage>= constants.L2thresh:
		GPIO.output(12,True)
	if voltage >= constants.L3thresh:
		GPIO.output(13,True)
	if voltage>= constants.L4thresh:
		GPIO.output(16,True)
	if voltage >= constants.L5thresh:
		GPIO.output(19,True)
	if voltage>= constants.L6thresh:
		GPIO.output(20,True)
	if voltage>= constants.L7thresh:
		GPIO.output(26,True)
	
	#L0 = GPIO 5
	#L1 = GPIO 6
	#L2 = GPIO 12
	#L3 = GPIO 13
	#L4 = GPIO 16
	#L5 = GPIO 19
	#L6 = GPIO 20
	#L7 = GPIO 26
	
def LDR():
	"""Repeatedly checks the value of the voltage from the LDR and adjusts the motor position based on this. Stops when automatic mode is turned off """
	import RPi.GPIO as GPIO
	import time
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(14,GPIO.OUT)
	pwm = GPIO.PWM(14,50)
	pwm.start(7.5)
	previousvoltage = findvoltage(0x21,0x10)
	try:	
		while automatic == True:
			switch()
			currentvoltage = findvoltage(0x21,0x10)

			if currentvoltage != None:
				if currentvoltage >= 2.9:
					pwm.ChangeDutyCycle(12.5)
					time.sleep(0.25)
					switch()
				elif currentvoltage <= 0.1:
					pwm.ChangeDutyCycle(2.5)
					time.sleep(0.25)
					switch()
				elif (currentvoltage+previousvoltage)/2 >= previousvoltage+0.1 or (currentvoltage+previousvoltage)/2 <= previousvoltage+0.1:
					pwm.ChangeDutyCycle(2.5+((10/3)* currentvoltage))
					time.sleep(0.25)
					switch()
					previousvoltage = currentvoltage


	except KeyboardInterrupt:
		pwm.stop()
		GPIO.cleanup() 


	


def Reset():
	"""Resets all i2c pins to active high """
	import time
	import smbus	


	bus = smbus.SMBus(1)

	bus.write_byte(0x20,0xFF)

def switch():
	"""flips the state of automatic if the button is pressed"""
	import time
	import smbus
	import constants
	
	bus = smbus.SMBus(1)
	global automatic
	x = bus.read_byte(0x20)
	if constants.harddebounce == True:
		if "{0:b}".format(x)[5:6] =="1":
			automatic = not automatic
			bus.close()
			yellowled(False)
			 
	else:
		if softwaredebounce() == True:
			automatic = not automatic
			bus.close()
			yellowled(False)
		
		
def softwaredebounce():
	import smbus
	import time
	bus = smbus.SMBus(1)
	global automatic
	x = bus.read_byte(0x20)
	starttime = time.time()
	counter = 0
	while time.time() - starttime <= 0.01:
		if "{0:b}".format(x)[4:5] =="1":
			counter += 1
			time.sleep(0.0001)
		else:
			counter = 0
			time.sleep(0.0001)
		
		if counter >= 10:
			return True
		
def Initialise():
	"""initializes the LEDS on the i2c and the PI and toggles the PWM on for the GUI."""
	yellowled(False)
	PWMtoggle()
	initialiselights()

def PWMtoggle(toggle):
	"""toggles the PWM on or off"""
	import RPi.GPIO as GPIO
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(10,GPIO.OUT)

	GPIO.output(10,toggle)

def Finish():
	"""cleans up any loose GPIOs and stops the pwm if necessary"""
	import RPi.GPIO as GPIO
	GPIO.setmode(GPIO.BCM)
	try:
		GPIO.cleanup()
	except:
		pass
	try:
		pwm.stop()
	except:
		pass

	
def setbool(var,string):
	"""swaps a boolean value var with not and sets the string to that value"""
	var.set(not var.get())
	string.set(str(var.get()))

def bugthread():
	import time
	clocktime = time.time()
	while  bugdetectiononnotgui == True:
		if time.time() - clocktime >= 4:
			global bugsdetectedcam
			bugsdetectedcam += blobdetection()
			clocktime = time.time()

	return
	
def Bugdoublefunc(var,string):
	"""runs the bug detection while the gui boolean is true"""
	setbool(var,string)
	global bugdetectiononnotgui
	if Bugdetectionon.get() == True:
		
		bugdetectiononnotgui = True
		t = threading.Thread(target = bugthread)
		t.start()
	else:
		bugdetectiononnotgui = False
		

def micthread():
	global Micdetectionnotgui 
	while Micdetectionnotgui == True:
		global bugsdetectedmic
		bugsdetectedmic+=bugdetectmic()
	
	return
		
def Micdoublefunc(var,string):
	"""runs the microphone detection while the gui boolean is true """
	setbool(var,string)
	if Micdetectionon.get() == True:
		Micdetectionnotgui = True
		t = threading.Thread(target = micthread)
		t.start()
	else:
		Micdetectionnotgui = False


		
def updatepwm(var,string):
	"""updates the PWM status when the gui button is pressed"""
	setbool(var,string)
	PWMtoggle(PWMstatus.get())
	

def updateauto(var,string):
	"""changes whether automatic is on or off"""
	setbool(var,string)
	global automatic
	automatic = automaticgui.get()


def endwindow():
	"""ends the window and calls the csv detection log"""
	primarywindow.destroy()		

def snap():
	global overridesnap
	overridesnap.set(True)
	overridesnapstring.set(str(overridesnap.get()))
	blobdetection()
	overridesnap.set(False)
	overridesnapstring.set(str(overridesnap.get()))

import tkinter as tk
from functools import partial



primarywindow = tk.Tk()
primarywindow.geometry("560x240")

camerastatus = tk.BooleanVar(primarywindow,value=0)
camerastring = tk.StringVar(primarywindow,value=str(camerastatus.get()))

micstatus = tk.BooleanVar(primarywindow,value=0)
micstring = tk.StringVar(primarywindow,value=str(micstatus.get()))

cockroachmic = tk.IntVar(primarywindow,value=0)
roachmicstring = tk.StringVar(primarywindow,value=str(cockroachmic.get()))

cockroachcam = tk.IntVar(primarywindow,value=0)
roachcamstring = tk.StringVar(primarywindow,value=str(cockroachcam.get()))

automaticgui = tk.BooleanVar(primarywindow,value=automatic)
automaticstring= tk.StringVar(primarywindow,value=str(automaticgui.get()))

PWMstatus = tk.BooleanVar(primarywindow,value=1)
PWMstring = tk.StringVar(primarywindow,value=str(PWMstatus.get()))

overridesnap = tk.BooleanVar(primarywindow,value = 0)
overridesnapstring = tk.StringVar(primarywindow,str(overridesnap.get()))

bugdetectiononnotgui = False
Bugdetectionon = tk.BooleanVar(primarywindow,value=0)
Bugdetectionstring = tk.StringVar(primarywindow,value=str(Bugdetectionon.get()))

Micdetectionnotgui = False
Micdetectionon = tk.BooleanVar(primarywindow,value=0)
Micdetectionstring = tk.StringVar(primarywindow,value=str(Micdetectionon.get()))

L1 = tk.Label(primarywindow,text="Camera status: ").grid(row=0,column=0)
A1 = tk.Label(primarywindow,textvariable=camerastring).grid(row=0,column=1)

L2 = tk.Label(primarywindow,text="Microphone status: ").grid(row=1,column=0)
A2 = tk.Label(primarywindow,textvariable=micstring).grid(row=1,column=1,)

L3 = tk.Label(primarywindow,text="Cockroaches detected by the microphone: ").grid(row=2,column=0)
A3 = tk.Label(primarywindow,textvariable = roachmicstring).grid(row=2,column=1)

L4 = tk.Label(primarywindow,text = "Cockroaches detected by the camera: ").grid(row=3,column=0)
A4 = tk.Label(primarywindow,textvariable = roachcamstring).grid(row=3,column=1)

L5 = tk.Label(primarywindow,text = "Motor in automatic mode: ").grid(row=4,column=0)
A5 = tk.Button(primarywindow,textvariable = automaticstring,command= partial(updateauto,automaticgui,automaticstring)).grid(row=4,column=1)

L6 = tk.Label(primarywindow,text = "PWM on: ").grid(row=5,column=0)
A6 = tk.Button(primarywindow,textvariable= PWMstring,command= partial(updatepwm,PWMstatus,PWMstring)).grid(row=5,column=1)

L7 = tk.Label(primarywindow,text = "Snap").grid(row=6,column=0)
A7 = tk.Button(primarywindow,textvariable=overridesnapstring, command= snap).grid(row=6,column=1)

L8 = tk.Label(primarywindow, text = "Camera Bug Detection").grid(row=0,column = 3,padx=50)
A8 = tk.Button(primarywindow, textvariable = Bugdetectionstring, command =partial(Bugdoublefunc,Bugdetectionon,Bugdetectionstring)).grid(row=0,column=4)

L9 = tk.Label(primarywindow,text = "Microphone Bug Detection").grid(row=1,column=3)
A9 = tk.Button(primarywindow,textvariable = Micdetectionstring, command = partial(Micdoublefunc,Micdetectionon,Micdetectionstring)).grid(row=1,column=4)


A10 = tk.Button(primarywindow,text="Exit",command = endwindow).grid(row=8,column=4)


		
Initialise()

#main bulk of code begins below
try:		
	if constants.bugdetectioncam == True:
		while True:
			bugs = blobdetection()
			if bugs != False:
				bugsdetectedcam += bugs


	if constants.bugdetectionmic == True:
		while True:
			bugs = bugdetectmic()
			if bugs == True:
				bugsdetectedmic += 1


	if constants.motor == True:
		while True:
			if automatic == True:
				LDR()
			else:
				time.sleep(0.25)
				switch()
	
	if constants.GUI == True:
		primarywindow.mainloop()



except KeyboardInterrupt:
	from time import strftime
	detectionlog = open("detectionlog.csv","a")
	
	if bugsdetectedcam > 0:
		detectionlog.write(strftime("%Y-%m-%d %H:%M:%S") +"," + str(bugsdetectedcam)+" bugs detected by camera")
	if bugsdetectedmic > 0:
		detectionlog.write(strftime("%Y-%m-%d %H:%M:%S") +"," + str(bugsdetectedmic)+" bugs detected by the microphone") 
	
	detectionlog.close()
	

Finish()
