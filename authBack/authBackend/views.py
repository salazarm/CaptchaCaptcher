# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
import random
def generate(request):
    charSet = ['1','2','3','4','5','6','7','8','9','10']
    random.shuffle(charSet)
    request.session['ans'] = 

    if request.method == 'POST':
        #here is where u verify

    return HttpResponse('application/javascript')
