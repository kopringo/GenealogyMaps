from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User

import numpy as np

# Create your views here.
from .models import Parish, Diocese, Province, County, Deanery, Source, ParishSource, ParishUser, Country, SOURCE_GROUP, RELIGION_TYPE
from .forms import ParishSourceForm, ParishEditForm, ParishMessageForm
from .decorators import group_required

def __prepare_common_params():
    return {
        'main_menu': 'churches',
        'body_map': True
    }


def set_param(request):
    theme = request.GET.get('theme', None)
    if theme is not None:
        request.session['theme'] = theme

    next_url = request.GET.get('next', '/')
    return redirect(next_url)


def get_religion_area(hp):
    ret = []
    for country in Country.objects.filter(historical_period=hp, public=True):
        for RL in RELIGION_TYPE:
            if Diocese.objects.filter(country=country, religion=RL[0]).count() > 0:
                ret.append([country.code, RL[0], RL[1]])
    return ret


def home0(request, data):
    # favourite
    if request.user.is_authenticated:
        data['favorite_list'] = ParishUser.objects.filter(user=request.user, favorite=True).select_related(
            'parish').all()
        data['manager_list'] = ParishUser.objects.filter(user=request.user, manager=True).select_related(
            'parish').all()

    periods = []

    periods.append([
        1, 'I Rzeczpospolita (1569-1795)',
        Country.objects.filter(public=True, historical_period=1),
        get_religion_area(1),
    ])

    periods.append([
        2, 'II Rzeczpospolita (1918-1945)',
        Country.objects.filter(public=True, historical_period=2),
        get_religion_area(2),
    ])

    periods.append([
        3, 'III Rzeczpospolita (1945-)',
        Country.objects.filter(public=True, historical_period=3),
        get_religion_area(3),
    ])

    periods.append([
        4, 'Okres zaborów',
        Country.objects.filter(public=True, historical_period=4),
        get_religion_area(4),
    ])

    data['periods'] = periods

    data['stats'] = {
        'parish_count': Parish.objects.count(),
        'source_count': ParishSource.objects.count(),
    }

    return render(request, 'core/home0.html', data)


def home(request):
    data = __prepare_common_params()
    data.update(_load_root_items())

    # points = np.array([[51.44502, 20.294522], [51.448337, 20.339841], [51.432501, 20.298299], [51.415481, 20.309285], [51.417944, 20.330228]])
    # hull = np.array(convex_hull(points))
    # data['test_ch'] = hull

    try:
        country = Country.objects.get(code=request.GET.get('country', None))
    except:
        country = None

    if country is None:
        return home0(request, data)

    else:
        data['limit_parish_on_the_map'] = '?lt=country&lv={}'.format(country.id)

        try:
            data['country'] = country
            religion = request.GET.get('religion', None)

            if religion is not None:
                data['dioceses'] = country.get_dioceses(religion)
            else:
                data['provinces'] = country.get_provinces()

        except:
            pass

        return render(request, 'core/home.html', data)


def validation_required(request):
    return render(request, 'core/validation_required.html')


def contact(request):
    return render(request, 'core/contact.html')


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


def _load_root_items():
    data ={}
    data['countries'] = Country.objects.all().filter(public=True)
    return data


def __get_convex_hull(items):
    try:
        points = []
        for item in items:
            if (item['geo_lat'] is not None) and (['geo_lng'] is not None):
                points.append([item['geo_lat'], item['geo_lng']])
    
        points = np.array(points)
        hull = np.array(convex_hull(points))
        return hull
    except Exception as e:
        print(e)
        return np.array([])

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
