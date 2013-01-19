## Imports needed to run 
from PIL import Image, ImageFont, ImageDraw 
import math 

## Making clock drawing function based on combineImage.py
def drawLines(imageLoc,numbers,width,height,r,x,y,saveLoc):
	n = len(numbers) # init vars 
	#new_im = Image.new('RGBA', (width,height),(255,255,255,0)) # draw canvas 
	new_im = Image.open(imageLoc)
	new_im.convert('RGBA')
	new_im.thumbnail((width,height))
	draw = ImageDraw.Draw(new_im)
	# draw.ellipse((x-r, y-r, x+r, y+r)) # draw circle 

	# Use n to generate the angles 
	increment = 2.0*math.pi/n
	angles = [] 
	last = 0 
	for i in range(n): 
		angles.append(last+increment)
		last = last+increment

	# # Draw all angle lines 
	# for i in range(n): 
	# 	draw.line([(x,y),(x+r*math.cos(angles[i]+math.pi/2.0),y+r*math.sin(angles[i]+math.pi/2.0))])

	# Paint numbers as a clock 
	for i in range(n): 
		draw.text((x+r*math.cos(angles[i]+math.pi/2.0),y+r*math.sin(angles[i]+math.pi/2.0)),str(numbers[i]),fill='black')

	new_im.save(saveLoc)
	new_im.show()

	# Calculate displacements to send
	tuples = zip(numbers,angles)
	d = dict()
	for t in range(len(tuples)): 
		d[tuples[t][0]] = (tuples[t][1]-math.pi)*50/math.pi
	print d

	return d 

def pasteImages(baseLock,numberLayer,outfile):
	img = Image.open(numberLayer)
	layer = Image.open(baseLock) # this file is the transparent one
	layer.thumbnail((300,300))
	print layer.mode # RGBA
	xoff = 0 
	yoff = 0
	img.paste(layer, (xoff, yoff), mask=layer) 
	# the transparancy layer will be used as the mask
	img.show()
	img.save(outfile)

def showFile(file): 
	img = Image.open(file)
	img.convert('RGBA')
	img.show()
	img.save('lock2.png')

# Sample usage 
x = 150 
y = 150 
r = 100
n = 24
width = 300 
height = 300 
numbers = [] 
for i in range(1,1+n): 
	numbers.append(i) 
drawLines('lock.png',numbers,width,height,r,width/2-5,height/2-5,'test.png')

#pasteImages('lock.png','test.png','combined.png')
#showFile('lock.png')