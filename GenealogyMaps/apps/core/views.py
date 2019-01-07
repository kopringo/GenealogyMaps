from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Parish, Diocese, Province


@login_required
def home(request):
    data = {}
    #data['parishes'] = Parish.objects.all()[0:2000]
    data.update(_load_root_items())
    return render(request, 'core/home.html', data)


def contact(request):
    return render(request, 'core/contact.html')


def _load_root_items():

    data = {
        'wojewodztwa': [],
        'diecezje': []
    }

    data['wojewodztwa'] = Province.objects.all()
    data['diecezje'] = Diocese.objects.all()

    return data
