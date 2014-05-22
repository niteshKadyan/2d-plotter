import Adafruit_BBIO.GPIO as GPIO 
import time 
import sys
import math
import serial

#bipolar
GPIO.setup("P8_7", GPIO.OUT)
GPIO.setup("P8_8", GPIO.OUT)
GPIO.setup("P8_9", GPIO.OUT)
GPIO.setup("P8_10", GPIO.OUT)

#unipolar
GPIO.setup("P9_11", GPIO.OUT)
GPIO.setup("P9_12", GPIO.OUT)
GPIO.setup("P9_13", GPIO.OUT)
GPIO.setup("P9_14", GPIO.OUT)

a = 0
stepu = 0
stepb = 0

def rotateBipolar(step, off_time):

	b = (step % 4) + 1
	
	if b == 1:
		GPIO.output("P8_7", GPIO.LOW)
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.HIGH)
		GPIO.output("P8_10", GPIO.LOW)

	if b == 2:
		GPIO.output("P8_7", GPIO.HIGH)
		GPIO.output("P8_8", GPIO.LOW)
		GPIO.output("P8_9", GPIO.HIGH)
		GPIO.output("P8_10", GPIO.LOW)

	if b == 3:
		GPIO.output("P8_7", GPIO.HIGH)
		GPIO.output("P8_8", GPIO.LOW)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_10", GPIO.HIGH)

	if b == 4:
		GPIO.output("P8_7", GPIO.LOW)
		GPIO.output("P8_8", GPIO.HIGH)
		GPIO.output("P8_9", GPIO.LOW)
		GPIO.output("P8_10", GPIO.HIGH)

	#time.sleep(off_time)

def rotateUnipolar(step, off_time):

	b = (step % 4) + 1

	if b == 1:
		GPIO.output("P9_11", GPIO.HIGH)
		GPIO.output("P9_12", GPIO.LOW)
		GPIO.output("P9_13", GPIO.LOW)
		GPIO.output("P9_14", GPIO.HIGH)

	if b == 2:
		GPIO.output("P9_11", GPIO.HIGH)
		GPIO.output("P9_12", GPIO.LOW)
		GPIO.output("P9_13", GPIO.HIGH)
		GPIO.output("P9_14", GPIO.LOW)

	if b == 3:
		GPIO.output("P9_11", GPIO.LOW)
		GPIO.output("P9_12", GPIO.HIGH)
		GPIO.output("P9_13", GPIO.HIGH)
		GPIO.output("P9_14", GPIO.LOW)

	if b == 4:
		GPIO.output("P9_11", GPIO.LOW)
		GPIO.output("P9_12", GPIO.HIGH)
		GPIO.output("P9_13", GPIO.LOW)
		GPIO.output("P9_14", GPIO.HIGH)

	#time.sleep(off_time)

def drawLine(x1, y1, directionx, directiony, off_time):

	global stepu, stepb
	slope = 0
	x = 1
	y = 1
	if x1 >= y1: 
		slope = y1/x1
		yprev = 0.0	
		while(x <= x1):
			y = slope * x
			print x, y
			if(round(y) > yprev):
				print "y = ", y
				if(directiony == 1):
					stepb += 1
				else:					
					stepb -= 1
				rotateBipolar(stepb, off_time)
				yprev = yprev + 1
				print "bipolar rotated with x >= y"
			x += 1
			if(directionx == 1):
				stepu += 1
			else:
				stepu -= 1
			rotateUnipolar(stepu, off_time)
			time.sleep(off_time)
			print "x = ", x

	else:
		slope = x1/y1
		xprev = 0.0
		while(y <= y1):
			x = slope * y
			if(round(x) > xprev):
				print " x = ", x

				if(directionx == 1):
	                                stepu += 1
				else:
					stepu -= 1
                                rotateUnipolar(stepu, off_time)
                                xprev = xprev + 1
				#print "unipolar rotated with x < y"
                        y += 1
			if(directiony == 1):
	                        stepb += 1
			else:
				stepb -= 1
                        rotateBipolar(stepb, off_time)
                        time.sleep(off_time)
			print "y = ", y

def drawCircle(div, radius):
	xold = 0.0
	yold = 0.0
	directionx = 1
	directiony = 1
	for i in range(0, div):
        	xx = math.cos(2 * math.pi / div * i) * radius
        	yy = math.sin(2 * math.pi / div * i) * radius

		x = abs(xx - xold)
		y = abs(yy - yold)

		xold = xx
		yold = yy

		if xx < 0:
			directionx = 1
		else:
			directionx = 0
		if yy < 0:
			directiony = 1
		else:
			directiony = 0
		print i, x, y
		if i != 0:
			drawLine(x, y, directiony, directionx, 0.05)

def main(argv):
	ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

	x = float(argv[0])
	y = float(argv[1])
	dx = float(argv[2])
	dy = float(argv[3])
	d = float(argv[4])

	#time.sleep(15)

#	drawLine(x, y, dx, dy, d)

	file = open("edges.txt", 'r')

	penUp = 0

	point = file.readline()
	xcurrent = 0
        ycurrent = 0

	point = point.split()
        x = float(point[0])
        y = float(point[1])

	ser.write("1")
	print ser.read()
	time.sleep(1)
	ser.write("1")

	drawLine(abs(x - xcurrent)*2.0, abs(y - ycurrent)*2.0, 0, 1, d)	
	
	ser.write("2")
	print ser.read()
	time.sleep(1)
	ser.write("2")

	xcurrent = x
	ycurrent = y

	while True:
		point = file.readline()

		if point == '':
			break
		point = point.split()
		x = float(point[0])
		y = float(point[1])


		if x == 1000.0:
			ser.write("1")
			print ser.read()
			time.sleep(1)
			penUp = 1
			x = xcurrent
			y = ycurrent
			continue

#		print x-xcurrent, y-ycurrent, dx, dy

		if x-xcurrent >= 0:
			dx = 0
		else:
			dx = 1

		if y-ycurrent >= 0:
			dy = 1
		else:
			dy = 0

		print "x y", x, y, dx, dy, "xcurrent", x - xcurrent, y - ycurrent
		drawLine(abs(x - xcurrent)*2.0, abs(y - ycurrent)*2.0, dx, dy, d)
	
		xcurrent = x
		ycurrent = y

		if penUp == 1:
			ser.write("2")
			print ser.read()
			time.sleep(1)
			penUp = 0

#		print x, y, dx, dy

	drawLine(abs(xcurrent)*2.0, abs(ycurrent)*2.0, 1, 0, d)
	time.sleep(1)
	
'''	for a in range(1, 200):
		if a%2 == 0:
			drawLine(1, 1, 0, 0, d)
		else:
			drawLine(1, 0, 0, 0, d)
'''		#print penUp
		#while True:
        	#rotateClockWise(200, d)
	        #time.sleep(1)
		#rotateCounterClockWise(200, d)
		#time.sleep(1)
		#drawLine(x, y, dx, dy, d)
		#drawCircle(100, 200.0)
#	drawLine(x, y, dx, dy, d)

if __name__ == "__main__":
    main(sys.argv[1:])
