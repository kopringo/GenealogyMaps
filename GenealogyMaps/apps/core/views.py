from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime

import numpy as np

# Create your views here.
from .models import Parish, Diocese, Province, County, Deanery, DocumentGroup
from .forms import DocumentGroupForm


@login_required
def home(request):
    data = {}
    data.update(_load_root_items())

    points = np.array([[51.44502, 20.294522], [51.448337, 20.339841], [51.432501, 20.298299], [51.415481, 20.309285], [51.417944, 20.330228]])
    hull = np.array(convex_hull(points))
    data['test_ch'] = hull

    return render(request, 'core/home.html', data)


def diocese(request, d_id):

    try:
        diocese = Diocese.objects.get(pk=d_id)
    except Diocese.DoesNotExist:
        return redirect('home')

    items = list(map(lambda x: {'name': x.name, 'link': '/area/deanery/%d' % x.id}, Deanery.objects.filter(diocese=diocese)))
    data = {
        'items': items,
        'diocese': diocese
    }
    return render(request, 'core/diocese.html', data)

def deanery(request, d_id):

    try:
        deanery = Deanery.objects.get(pk=d_id)

    except Deanery.DoesNotExist:
        pass

    items = list(map(lambda x: {'name': '%s, %s' % (x.place, x.name), 'link': '/parish/%d' % x.id}, Parish.objects.filter(deanery=deanery)))
    data = {
        'items': items,
        'deanery': deanery
    }
    return render(request, 'core/deanery.html', data)

def province(request, p_id):
    """
    Show the provice

    :param request:
    :param p_id: province id
    """
    try:
        province = Province.objects.get(pk=p_id)
    except Province.DoesNotExist:
        return redirect('home')


    counties = list(map(lambda x: {'name': x.name, 'link': '/area/county/%d' % x.id}, County.objects.filter(province=province)))
    items = __get_parish_list(province=province)

    convex_hull = __get_convex_hull(items)

    data = {
        'counties': counties,
        'items': items,
        'province': province,
        'convex_hull': convex_hull
    }
    return render(request, 'core/province.html', data)


def county(request, c_id):

    try:
        county = County.objects.get(pk=c_id)
    except County.DoesNotExist:
        return redirect('home')

    items = __get_parish_list(county=county)
    data = {
        'items': items,
        'county': county
    }
    return render(request, 'core/county.html', data)


def parish(request, parish_id):
    parish = Parish.objects.get(pk=parish_id)
    documents = DocumentGroup.objects.filter(parish=parish).order_by('date_from')
    #comments =
    return render(request, 'core/parish.html', {'parish': parish, 'document_groups': documents})


def parish_list_json(request):
    _items = list(Parish.objects.values('id', 'name', 'geo_lat', 'geo_lng', 'province__id', 'county__id', 'place', 'address'))
    items = {}
    for _item in _items:
        items[_item['id']] = _item

    return JsonResponse(items)


def document_add(request, parish_id):
    form = DocumentGroupForm()
    saved = False

    # pobranie parafii
    try:
        parish = Parish.objects.get(pk=parish_id)
    except Parish.DoesNotExist:
        return redirect('/?error=parish-not-exits')

    # document group jesli edytujemy
    dg = request.GET.get('dg', request.POST.get('dg', None))
    document_group = None
    if dg is not None:
        try:
            document_group = DocumentGroup.objects.get(pk=dg, parish=parish)
            form = DocumentGroupForm(instance=document_group)
        except DocumentGroup.DoesNotExist:
            pass

    if request.method == 'POST':
        form = DocumentGroupForm(request.POST, instance=document_group)

        if form.is_valid():
            document_group = form.save(commit=False)
            document_group.parish = parish
            document_group.user = request.user
            document_group.save()
            if document_group is None:
                document_group.date_created = datetime.utcnow()
            else:
                document_group.date_modified = datetime.utcnow()

            parish.refresh_summary()

            saved = True

    return render(request, 'parts/document_add.html', {'form': form, 'saved': saved, 'parish': parish, 'document_group': document_group})

def documents(request, parish_id):

    return render(request, 'parts/documents.html', { 'parish': parish})


def contact(request):
    return render(request, 'core/contact.html')


def profile(request):
    return render(request, 'accounts/profile.html')


def _load_root_items():
    data ={}
    data['provinces'] = Province.objects.all().filter(public=True)
    data['dioceses'] = Diocese.objects.all().filter(public=True)
    return data


def __get_parish_list(**args):
    return list(map(lambda x: {
        'name': x.name,
        'place': x.place,
        'link': '/parish/%d' % x.id,
        'id': x.id,
        'year': x.year,
        'place': x.place,
        'geo_lat': x.geo_lat,
        'geo_lng': x.geo_lng
    }, Parish.objects.filter(**args)))


def __get_convex_hull(items):
    points = []
    for item in items:
        points.append([item['geo_lat'], item['geo_lng']])

    points = np.array(points)
    hull = np.array(convex_hull(points))
    return hull

####
# https://www.oreilly.com/ideas/an-elegant-solution-to-the-convex-hull-problem


def split(u, v, points):
    # return points on left side of UV
    return [p for p in points if np.cross(p - u, v - u) < 0]


def extend(u, v, points):
    if not points:
        return []

    # find furthest point W, and split search to WV, UW
    w = min(points, key=lambda p: np.cross(p - u, v - u))
    p1, p2 = split(w, v, points), split(u, w, points)
    return extend(w, v, p1) + [w] + extend(u, w, p2)


def convex_hull(points):
    # find two hull points, U, V, and split to left and right search
    u = min(points, key=lambda p: p[0])
    v = max(points, key=lambda p: p[0])
    left, right = split(u, v, points), split(v, u, points)

    # find convex hull on each side
    return [v] + extend(u, v, left) + [u] + extend(v, u, right) + [v]
