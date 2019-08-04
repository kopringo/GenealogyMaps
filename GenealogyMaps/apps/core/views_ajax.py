from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http.response import JsonResponse

# Create your views here.
from .models import Source, Parish

@login_required
def sources(request):

    data = {'results': [], 'pagionation': {}}
    group = request.GET.get('g', None)
    q = request.GET.get('q', None)
    
    items = None
    if group == 'PAR': # archiwum parafialne, dajemy parafie a nie archiwa!
        items = Parish.objects.all().filter(Q(name__icontains=q)|Q(place__icontains=q)).order_by('province__name', 'place', 'name')
        
        for item in items:
            data['results'].append({'id': item.id, 'text': '%s, %s: %s' % (str(item.province), item.place, item.name) })

    elif group is not None:
        items = Source.objects.all().filter(group=group).order_by('name')
        if q is not None:
            items = items.filter(name__icontains=q)

        for item in items:
            data['results'].append({'id': item.id, 'text': item.name})

    return JsonResponse(data)

@login_required
def parishes(request):
    q = request.GET.get('q', None)
    data = {'results': [], 'pagionation': {}}
    if q is not None and len(q) >=3:
        items = Parish.objects.all().filter(Q(name__icontains=q) | Q(place__icontains=q)).order_by('province__name', 'place', 'name')
        for item in items:
            data['results'].append({'id': item.id, 'text': '%s, %s: %s (%d)' % (str(item.province), item.place, item.name, item.year)})

    return JsonResponse(data)