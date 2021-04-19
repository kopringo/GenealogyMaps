from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User

import numpy as np

# Create your views here.
from .models import Parish, Diocese, Province, County, Deanery, Source, ParishSource, ParishUser, Country, SOURCE_GROUP
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


def home(request):
    data = __prepare_common_params()
    data.update(_load_root_items())

    points = np.array([[51.44502, 20.294522], [51.448337, 20.339841], [51.432501, 20.298299], [51.415481, 20.309285], [51.417944, 20.330228]])
    hull = np.array(convex_hull(points))
    data['test_ch'] = hull

    # favourite
    if request.user.is_authenticated:
        data['favorite_list'] = ParishUser.objects.filter(user=request.user, favorite=True).select_related('parish').all()
        data['manager_list'] = ParishUser.objects.filter(user=request.user, manager=True).select_related('parish').all()

    try:
        data['country'] = Country.objects.get(code=request.GET.get('country', None))
    except:
        pass

    data['stats'] = {
        'parish_count': Parish.objects.count(),
        'source_count': ParishSource.objects.count(),
    }

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
            points.append([item['geo_lat'], item['geo_lng']])
    
        points = np.array(points)
        hull = np.array(convex_hull(points))
        return hull
    except:
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
