from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import numpy as np

# Create your views here.
from .models import Parish, Diocese, Province


@login_required
def home(request):
    data = {}
    #data['parishes'] = Parish.objects.all()[0:2000]
    data.update(_load_root_items())

    points = np.array([[51.44502, 20.294522], [51.448337, 20.339841], [51.432501, 20.298299], [51.415481, 20.309285], [51.417944, 20.330228]])
    hull = np.array(convex_hull(points))
    data['test_ch'] = hull

    return render(request, 'core/home.html', data)


def contact(request):
    return render(request, 'core/contact.html')


def profile(request):
    return render(request, 'accounts/profile.html')


def _load_root_items():

    data = {
        'wojewodztwa': [],
        'diecezje': []
    }

    data['wojewodztwa'] = Province.objects.all()
    data['diecezje'] = Diocese.objects.all()

    return data



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
