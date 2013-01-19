# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
import random

## Imports needed to run 
from PIL import Image, ImageFont, ImageDraw 
import math 

## Making clock drawing function based on combineImage.py
def drawLines(numbers,width,height,r,x,y,saveLoc):
    n = len(numbers) # init vars 
    new_im = Image.new('RGBA', (width,height),(255,255,255,0)) # draw canvas 
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
    #   draw.line([(x,y),(x+r*math.cos(angles[i]+math.pi/2.0),y+r*math.sin(angles[i]+math.pi/2.0))])

    # Paint numbers as a clock 
    for i in range(n): 
        draw.text((x+r*math.cos(angles[i]+math.pi/2.0),y+r*math.sin(angles[i]+math.pi/2.0)),str(numbers[i]),fill='blue')

    png_info = new_im.info
    new_im.save(saveLoc, **png_info)
    


 

def generate(request):
    charSet = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20', '21','22','23','24','25', 'a','b','c','d','e','f''g']
    
    randSet = []
    setLen = 24
    for i in range(setLen):
        randNum = random.randint(0,len(charSet)-1)
        randSet.append(charSet[randNum])
        del charSet[randNum]

    random.shuffle(randSet)

    imageUrl = 'lock.png'
    

    # Sample usage 
    x = 150 
    y = 150 
    r = 125
    n = 24
    width = 300 
    height = 300  
    angles = drawLines(randSet,width,height,r,width/2,height/2,'/Users/prabhav/Documents/development/pennapps/authBack/static/lock.png')


    #get image back
    randNum = random.randint(0,setLen-1)
    ans = randSet[randNum]

    #calculate offset
    request.session['ans-offset'] = angles[ans]

   


    errorDisp = 5
    if request.is_ajax():
        #here is where u verify

        avg = float(request.POST.get('avg'))

        if abs(avg - request.session['ans-offset']) < errorDisp:
            json = simplejson.dumps( [{'status': '1'}])
            return HttpResponse(json, 'application/javascript')


            


    return render_to_response('lock.html', {'img': imageUrl, 'ans' : ans}, context_instance=RequestContext(request))
    
