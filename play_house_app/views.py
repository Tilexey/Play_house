from django.shortcuts import render
from .models import *


# Create your views here.
def hall_list(request):
    halls = Hall.objects.all()
    return render(request, 'hall_list.html', {'halls': halls})