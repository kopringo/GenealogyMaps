from django.shortcuts import render

# Create your views here.
from .models import Parish, Diocese, Province


def root(request):
    data = {}
    data.update(_load_root_items())
    return render(request, 'parts/root.html', data)


def

def _load_root_items():

    data = {
        'wojewodztwa': [],
        'diecezje': []
    }

    data['wojewodztwa'] = Province.objects.all()
    data['diecezje'] = Diocese.objects.all()

    return data
