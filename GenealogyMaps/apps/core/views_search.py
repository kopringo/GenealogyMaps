from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
from .models import Parish

@login_required
def index(request):

    data = {}
    q = request.GET.get('q', None)
    if q is None:
        return redirect('/')
    if len(q) < 3:
        return redirect('/?error=to-short')
    parishes = Parish.objects.filter(Q(name__icontains=q) | Q(place__icontains=q))
    data['parishes'] = parishes

    return render(request, 'core/_search/index.html', data)
