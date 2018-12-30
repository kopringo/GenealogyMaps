
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from .models import Parish, Diocese, Province


def parishes__get(request):
    data = {
        'parishes': list(Parish.objects.values('id', 'name', 'geo_lat', 'geo_lng').all()[0:2000])
    }
    response = JsonResponse(data)
    return response

