# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
import random

def generate(request):
    charSet = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20', '21','22','23','24','25', 'a','b','c','d','e','f''g']
    
    randSet = []
    setLen = 24
    for i in range(setLen):
        randNum = random.randint(0,len(charSet)-1)
        randSet.append(charSet[randNum])
        del charSet[randNum]

    random.shuffle(randSet)

    #send rand array to jesika's pil

    #get image back

    ans = '5'

    #send image to client

    imageUrl = 'lock.png'
    request.session['ans-offset'] = '20'

    errorDisp = 5
    if request.is_ajax():
        #here is where u verify

        avg = int(request.POST.get('avg'))

        if abs(avg - request.session['ans-offset']) < errorDisp:
            return HttpResponseRedirect('/win')
            


    return render_to_response('lock.html', {'img': imageUrl, 'ans' : ans}, context_instance=RequestContext(request))
    
