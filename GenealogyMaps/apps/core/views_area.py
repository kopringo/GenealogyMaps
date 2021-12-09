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
from .views import convex_hull, __get_convex_hull


def __prepare_common_params():
    return {
        'main_menu': 'churches',
        'body_map': True
    }


@group_required('DATA_ACCESS')
def diocese(request, d_id):
    """ Diecezja """

    try:
        diocese = Diocese.objects.get(pk=d_id)
    except Diocese.DoesNotExist:
        return redirect('home')

    deaneries = list(map(lambda x: {'name': x.name, 'link': '/area/deanery/%d' % x.id}, Deanery.objects.filter(diocese=diocese).order_by('name')))
    if diocese.country.historical_period == 1:
        items = __get_parish_list(deanery_r1__diocese=diocese)
    if diocese.country.historical_period == 2:
        items = __get_parish_list(deanery_r2__diocese=diocese)
    if diocese.country.historical_period == 3: # 3 rp
        items = __get_parish_list(diocese=diocese)
    if diocese.country.historical_period == 4:
        items = __get_parish_list(deanery_rz__diocese=diocese)


    convex_hull = __get_convex_hull(items)

    data = __prepare_common_params()
    data['load_full_map'] = True
    data.update({
        'diocese': diocese,
        'deaneries': deaneries,
        'items': items,
        'convex_hull': convex_hull,
        'limit_parish_on_the_map': '?lt=diocese&lv={}&lhp={}'.format(d_id, diocese.country.historical_period),
    })

    return render(request, 'core/diocese.html', data)


@group_required('DATA_ACCESS')
def deanery(request, d_id):
    """ Dekanat """

    try:
        deanery = Deanery.objects.get(pk=d_id)

    except Deanery.DoesNotExist:
        pass

    if deanery.diocese.country.historical_period == 1:
        items = __get_parish_list(deanery_r1=deanery)
    if deanery.diocese.country.historical_period == 2:
        items = __get_parish_list(deanery_r2=deanery)
    if deanery.diocese.country.historical_period == 3: # 3 rp
        items = __get_parish_list(deanery=deanery)
    if deanery.diocese.country.historical_period == 4:
        items = __get_parish_list(deanery_rz=deanery)

    convex_hull = __get_convex_hull(items)

    data = __prepare_common_params()
    data['load_full_map'] = True
    data.update({
        'items': items,
        'deanery': deanery,
        'convex_hull': convex_hull,
        'limit_parish_on_the_map': '?lt=deanery&lv={}&lhp={}'.format(d_id, deanery.diocese.country.historical_period),
    })
    return render(request, 'core/deanery.html', data)


@group_required('DATA_ACCESS')
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

    counties = list(map(lambda x: {'name': x.name, 'link': '/area/county/%d' % x.id}, County.objects.filter(province=province).order_by('name')))
    if province.country.historical_period == 1:
        items = __get_parish_list(county_r1__province=province)
    if province.country.historical_period == 2:
        items = __get_parish_list(county_r2__province=province)
    if province.country.historical_period == 3: # 3 rp
        items = __get_parish_list(province=province)
    if province.country.historical_period == 4:
        items = __get_parish_list(county_rz__province=province)

    convex_hull = __get_convex_hull(items)

    data = __prepare_common_params()
    data['load_full_map'] = True
    data.update({
        'counties': counties,
        'items': items,
        'province': province,
        'convex_hull': convex_hull,
        'limit_parish_on_the_map': '?lt=province&lv={}&lhp={}'.format(p_id, province.country.historical_period),
        'mapid_fixed': True
    })
    return render(request, 'core/province.html', data)


@group_required('DATA_ACCESS')
def county(request, c_id):

    try:
        county = County.objects.get(pk=c_id)
    except County.DoesNotExist:
        return redirect('home')
    if county.province.country.historical_period == 1:
        items = __get_parish_list(county_r1=county)
    if county.province.country.historical_period == 2:
        items = __get_parish_list(county_r2=county)
    if county.province.country.historical_period == 3: # 3 rp
        items = __get_parish_list(county=county)
    if county.province.country.historical_period == 4:
        items = __get_parish_list(county_rz=county)


    convex_hull = __get_convex_hull(items)

    data = __prepare_common_params()
    data['load_full_map'] = True
    data.update({
        'items': items,
        'county': county,
        'convex_hull': convex_hull,
        'limit_parish_on_the_map': '?lt=county&lv={}&lhp={}'.format(c_id, county.province.country.historical_period),
    })
    return render(request, 'core/county.html', data)

def __get_parish_list(**args):
    return list(map(lambda x: {
        'name': x.name,
        'place': x.place,
        'link': '/parish/%d' % x.id,
        'id': x.id,
        'year': x.year,
        'place': x.place,
        'geo_lat': x.geo_lat,
        'geo_lng': x.geo_lng,
        'any_issues': x.any_issues()
    }, Parish.objects.filter(**args).order_by('place', 'name')))
