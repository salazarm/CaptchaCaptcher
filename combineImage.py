
import math 	
from PIL import Image, ImageDraw, ImageFont

#opens an image:
im = Image.open("/Users/jesika/Pictures/jesika-ktse.png")
#creates a new empty image, RGB mode, and size 400 by 400.
new_im = Image.new('RGB', (300,300))

# #Here I resize my opened image, so it is no bigger than 100,100
# im.thumbnail((50,50))
# #Iterate through a 4 by 4 grid with 100 spacing, to place my image
# for i in xrange(0,500,100):
#     for j in xrange(0,500,100):
#         #I change brightness of the images, just to emphasise they are unique copies.
#         im=Image.eval(im,lambda x: x+(i+j)/30)
#         #paste the image at location i,j:
#         new_im.paste(im, (200,25))


# Font - bitmap 
# font = ImageFont.load("arial.pil")
# fontsize = 14
# font = ImageFont.load("False3D.ttf")
# draw.text((10, 10), "hello", font=font)



# Code for circle drawing 
x = 150 
y = 150 
r = 125
n = 24
numbers = [] 
for i in range(1,1+n): 
	numbers.append(i) 
n = len(numbers)
draw = ImageDraw.Draw(new_im)
draw.ellipse((x-r, y-r, x+r, y+r))

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

new_im.show()