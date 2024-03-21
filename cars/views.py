from django.shortcuts import render
from .models import Car

# Create your views here.

def index(request):
    context = {
        'cars': Car.objects.all().order_by('-id')
    }
    return render(request, "cars/index.html", context)
