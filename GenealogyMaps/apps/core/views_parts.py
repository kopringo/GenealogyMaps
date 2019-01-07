from django.shortcuts import render

# Create your views here.
from .models import Parish, Diocese, Province, County, Deanery


def root(request):
    data = {}
    data.update(_load_root_items())
    return render(request, 'parts/root.html', data)


def area(request):
    province_id = request.GET.get('province', None)
    county_id = request.GET.get('county', None)
    diocese_id = request.GET.get('diocese', None)
    deanary_id = request.GET.get('deanary', None)

    items = []

    try:
        province = Province.objects.get(pk=province_id)
        items = list(map(lambda x: {'name': x.name, 'link': '/parts/area?county=%d' % x.id}, County.objects.filter(province=province)))
    except Province.DoesNotExist:
        pass

    try:
        county = County.objects.get(pk=county_id)
        items = list(map(lambda x: {'name': x.name, 'link': '/api2/parishes/%d/?format=html' % x.id}, Parish.objects.filter(county=county)))
    except County.DoesNotExist:
        pass

    try:
        diocese = Diocese.objects.get(pk=diocese_id)
        items = list(map(lambda x: {'name': x.name, 'link': '/parts/area?diocese=' % x.id}, Deanery.objects.filter(diocese=diocese)))
    except Diocese.DoesNotExist:
        pass

    try:
        deanery = Deanery.objects.get(pk=deanary_id)
        items = list(map(lambda x: {'name': x.name, 'link': '/api2/parishes/%d/?format=html' % x.id}, Parish.objects.filter(deanery=deanery)))
    except Deanery.DoesNotExist:
        pass

    if len(items) == 0:
        return root(request)

    return render(request, 'parts/area.html', {'items': items})




def _load_root_items():

    data = {
        'provinces': [],
        'dioceses': []
    }

    data['provinces'] = Province.objects.all()
    data['dioceses'] = Diocese.objects.all()

    return data
