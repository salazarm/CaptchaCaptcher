## Imports needed to run 
from PIL import Image, ImageFont, ImageDraw 
import math 

## Making clock drawing function based on combineImage.py
def drawLines(numbers,width,height,r,x,y,saveLoc):
	n = len(numbers) # init vars 
	new_im = Image.new('RGB', (width,height)) # draw canvas 
	draw = ImageDraw.Draw(new_im)
	draw.ellipse((x-r, y-r, x+r, y+r)) # draw circle 

	# Use n to generate the angles 
	increment = 2.0*math.pi/n
	angles = [] 
	last = 0 
	for i in range(n): 
		angles.append(last+increment)
		last = last+increment

	# Draw all angle lines 
	for i in range(n): 
		draw.line([(x,y),(x+r*math.cos(angles[i]+math.pi/2.0),y+r*math.sin(angles[i]+math.pi/2.0))])

	# Paint numbers as a clock 
	for i in range(n): 
		draw.text((x+r*math.cos(angles[i]+math.pi/2.0),y+r*math.sin(angles[i]+math.pi/2.0)),str(numbers[i]))

	new_im.save(saveLoc,"JPEG")
	new_im.show()

# Sample usage 
x = 150 
y = 150 
r = 125
n = 24
width = 300 
height = 300 
numbers = [] 
for i in range(1,1+n): 
	numbers.append(i) 
drawLines(numbers,width,height,r,width/2,height/2,'test.jpg')