from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
def index(request):
    context = {

    }
    if 'contact_form' in request.POST:
        return HttpResponseRedirect('/gracias/')
    else:
        return render(request, 'index.html', context)

