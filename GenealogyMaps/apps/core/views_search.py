from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
from .models import Parish

def index(request):

    data = {}
    q = request.GET.get('q', None)
    hide_a_1800 = True if request.GET.get('hide_a_1800', None) is not None else False
    if q is None:
        return redirect('/')
    if len(q) < 3:
        return redirect('/?error=to-short')
    parishes = Parish.objects.filter(Q(place__icontains=q) | Q(place2__icontains=q) )
    if hide_a_1800:
        parishes = parishes.filter(year__lt=1800).exclude(year=0)
    parishes = parishes.order_by('year')
    data['parishes'] = parishes
    data['hide_search'] = True
    data['q'] = q
    data['hide_a_1800'] = hide_a_1800

    return render(request, 'core/_search/index.html', data)
