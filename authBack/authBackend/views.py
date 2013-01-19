# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
import random
from django.utils import simplejson
import json
import logging
import time

## Imports needed to run 
from PIL import Image, ImageFont, ImageDraw 
import math 

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
    #   draw.line([(x,y),(x+r*math.cos(angles[i]+math.pi/2.0),y+r*math.sin(angles[i]+math.pi/2.0))])

    # Paint numbers as a clock 
    for i in range(n): 
        draw.text((x+r*math.cos(angles[i]+math.pi/2.0),y+r*math.sin(angles[i]+math.pi/2.0)),str(numbers[i]),fill='black')

    new_im.save(saveLoc)
    #new_im.show()

    # Calculate displacements to send
    tuples = zip(numbers,angles)
    d = dict()
    for t in range(len(tuples)): 
        d[tuples[t][0]] = (tuples[t][1]-math.pi)*50/math.pi
    print d

    return d 
    


 

def generate(request):
    
    errorDisp = 3
    TIMEOUT = 60
    is_ajax_req = False
    totalNum = 3

    if 'num-correct' not in request.session or  request.session['num-correct'] >= 3:
        request.session['num-correct'] = 0
    if request.is_ajax():
        is_ajax_req = True
        is_correct = False
        #here is where u verify

        avg = float(request.POST.get('avg'))
        print "=========================" + str(avg)

        if time.time() - request.session['time'] <= TIMEOUT:
            if abs(avg - request.session['ans-offset']) < errorDisp:
                request.session['num-correct'] += 1
                is_correct = True
            

    charSet = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20', '21','22','23','24','25', 'a','b','c','d','e','f','g']
    
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
    r = 100
    n = 24
    width = 300 
    height = 300  
    angles = drawLines('/Users/prabhav/Documents/development/pennapps/authBack/static/lock_template.png',randSet,width,height,r,width/2-5,height/2-5,'/Users/prabhav/Documents/development/pennapps/authBack/static/lock.png')


    #get image back
    randNum = random.randint(0,setLen-1)
    ans = randSet[randNum]

    #calculate offset
    request.session['ans-offset'] = angles[ans]
    request.session['time'] = time.time()

    if is_ajax_req:
        if is_correct:
            json = simplejson.dumps( [{'status': 'corr','img': imageUrl, 'ans' : ans, 'left': totalNum -  request.session['num-correct']}])
        else:
            json = simplejson.dumps( [{'status': 'incorr','img': imageUrl, 'ans' : ans, 'left': totalNum - request.session['num-correct']}])
        return HttpResponse(json,content_type='application/json')

    return render_to_response('lock.html', {'img': imageUrl, 'ans' : ans}, context_instance=RequestContext(request))
    
