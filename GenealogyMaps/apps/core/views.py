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

@login_required
def home(request):
    data = __prepare_common_params()
    data.update(_load_root_items())

    points = np.array([[51.44502, 20.294522], [51.448337, 20.339841], [51.432501, 20.298299], [51.415481, 20.309285], [51.417944, 20.330228]])
    hull = np.array(convex_hull(points))
    data['test_ch'] = hull

    # favourite
    data['favorite_list'] = ParishUser.objects.filter(user=request.user, favorite=True).select_related('parish').all()
    data['manager_list'] = ParishUser.objects.filter(user=request.user, manager=True).select_related('parish').all()

    try:
        data['country'] = Country.objects.get(code=request.GET.get('country', None))
    except:
        pass

    return render(request, 'core/home.html', data)


@login_required
def diocese(request, d_id):
    """ Diecezja """

    try:
        diocese = Diocese.objects.get(pk=d_id)
    except Diocese.DoesNotExist:
        return redirect('home')

    deaneries = list(map(lambda x: {'name': x.name, 'link': '/area/deanery/%d' % x.id}, Deanery.objects.filter(diocese=diocese).order_by('name')))
    items = __get_parish_list(diocese=diocese)

    convex_hull = __get_convex_hull(items)

    data = __prepare_common_params()
    data.update({
        'diocese': diocese,
        'deaneries': deaneries,
        'items': items,
        'convex_hull': convex_hull
    })

    return render(request, 'core/diocese.html', data)


@login_required
def deanery(request, d_id):
    """ Dekanat """

    try:
        deanery = Deanery.objects.get(pk=d_id)

    except Deanery.DoesNotExist:
        pass

    #items = list(map(lambda x: {'name': '%s, %s' % (x.place, x.name), 'link': '/parish/%d' % x.id}, Parish.objects.filter(deanery=deanery)))
    items = __get_parish_list(deanery=deanery)
    convex_hull = __get_convex_hull(items)

    data = __prepare_common_params()
    data.update({
        'items': items,
        'deanery': deanery,
        'convex_hull': convex_hull
    })
    return render(request, 'core/deanery.html', data)


@login_required
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
    items = __get_parish_list(province=province)

    convex_hull = __get_convex_hull(items)

    data = __prepare_common_params()
    data.update({
        'counties': counties,
        'items': items,
        'province': province,
        'convex_hull': convex_hull
    })
    return render(request, 'core/province.html', data)


@login_required
def county(request, c_id):

    try:
        county = County.objects.get(pk=c_id)
    except County.DoesNotExist:
        return redirect('home')

    items = __get_parish_list(county=county)
    convex_hull = __get_convex_hull(items)

    data = __prepare_common_params()
    data.update({
        'items': items,
        'county': county,
        'convex_hull': convex_hull
    })
    return render(request, 'core/county.html', data)

#@group_required('DATA_ACCESS')
@login_required
def parish(request, parish_id):
    """ Widok parafii """
    try:
        parish = Parish.objects.get(pk=parish_id)
    except Parish.DoesNotExist:
        return redirect('home') # '?error=doesnotexist'
    documents = ParishSource.objects.filter(parish=parish).order_by('date_from')
    documents_sorted = __prepare_report(documents)
    documents_yby = __prepare_report_yby(documents)

    parish_user = None
    try:
        if request.user.is_authenticated:
            parish_user = ParishUser.objects.get(parish=parish, user=request.user)
    except ParishUser.DoesNotExist:
        pass

    # czy istnieje manager
    manager_exists = None
    try:
        manager_exists = ParishUser.objects.filter(parish=parish, manager=True)[0].user
    except:
        pass

    data = __prepare_common_params()
    data.update({
        'parish': parish,
        'document_groups': documents,
        'document_groups_sorted': documents_sorted,
        'document_groups_yby': documents_yby,
        'manager': parish.has_user_manage_permission(request.user),
        'managers': ParishUser.objects.filter(parish=parish, manager=True),
        'parish_user': parish_user,
        'manager_exists': manager_exists
    })

    return render(request, 'core/parish.html', data)


@login_required
def parish_edit(request, parish_id):
    """ Panel edycji parafii dla opiekuna """
    data = {}

    parish = Parish.objects.get(pk=parish_id)
    if not parish.has_user_manage_permission(request.user):
        return redirect('/?error=access-denied')

    form = ParishEditForm(instance=parish)

    if request.method == 'POST':
        form = ParishEditForm(request.POST, instance=parish)
        if form.is_valid():
            form.save()

            return redirect('/parish/%d' % parish.id)

    data.update({
        'parish': parish,
        'form': form
    })

    return render(request, 'core/parish_edit.html', data)


@login_required
def parish_message(request, parish_id):
    """ Panel edycji parafii dla opiekuna """
    data = {}

    parish = Parish.objects.get(pk=parish_id)
    saved = False
    form = ParishMessageForm()

    if request.method == 'POST':
        form = ParishMessageForm(request.POST)
        if form.is_valid():


            manager_exists = None
            try:
                manager_exists = ParishUser.objects.filter(parish=parish, manager=True)[0].user
            except:
                pass

            from django_messages.models import Message
            message = Message()
            message.subject = form.cleaned_data['title']
            message.body = form.cleaned_data['body']
            message.sender = request.user
            message.recipient = manager_exists
            message.sent_at = datetime.utcnow()
            message.save()

            saved = True



    data.update({
        'parish': parish,
        'form': form,
        'saved': saved
    })

    return render(request, 'core/parish_message.html', data)


def parish_list_json(request):
    _items = list(Parish.objects.filter(visible=True).values('id', 'name', 'geo_lat', 'geo_lng', 'province__id', 'county__id', 'place', 'address'))
    items = {}
    for _item in _items:
        items[_item['id']] = _item

    return JsonResponse(items)


def document_add(request, parish_id):
    form = ParishSourceForm()
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
            document_group = ParishSource.objects.get(pk=dg, parish=parish)
            form = ParishSourceForm(instance=document_group)
        except ParishSource.DoesNotExist:
            pass

    if request.method == 'POST':
        post = request.POST.copy()
        par = False
        # hack, jesli wybieramy archiwum parafialne to ustawiamy na sztywno source jeden
        # i relacja idzie do parish
        if post.get('source_type', None) == 'PAR':
            par = True
            post['source'] = Source.objects.filter(group='PAR')[0].id

        form = ParishSourceForm(post, instance=document_group)

        if form.is_valid():
            document_group = form.save(commit=False)
            document_group.parish = parish
            document_group.user = request.user

            if document_group is None:
                document_group.date_created = datetime.utcnow()
            else:
                document_group.date_modified = datetime.utcnow()

            if par:
                try:
                    document_group.source_parish = Parish.objects.get(pk=int(post.get('source_parish')))
                except:
                    pass

            document_group.save()
            parish.refresh_summary(True)

            saved = True

    source_types = SOURCE_GROUP

    data = {
        'form': form,
        'saved': saved,
        'parish': parish,
        'document_group': document_group,
        'source_types': source_types
    }
    return render(request, 'parts/document_add.html', data)


def documents(request, parish_id):
    parish = Parish.objects.get(pk=parish_id)
    documents = ParishSource.objects.filter(parish=parish).order_by('date_from')

    return render(request, 'parts/documents.html', {
        'parish': parish,
        'document_groups': documents,
        'manager': parish.has_user_manage_permission(request.user)
    })


def parish_favourite(request, parish_id):

    # trzeba byc zalogowanym
    if not request.user.is_authenticated:
        return render(request, 'parts/parish_favourite.html', {'error_user': True})

    try:
        parish = Parish.objects.get(pk=parish_id)
    except Parish.DoesNotExist:
        return render(request, 'parts/parish_favourite.html', {'error_parish': True})

    try:
        parish_user = ParishUser.objects.get(user=request.user, parish=parish)
    except ParishUser.DoesNotExist:
        parish_user = ParishUser()
        parish_user.user = request.user
        parish_user.parish = parish

    parish_user.favorite = not parish_user.favorite
    parish_user.save()

    return render(request, 'parts/parish_favourite.html', {
        'parish': parish,
        'parish_user': parish_user
    })


def parish_request_access(request, parish_id):

    # trzeba byc zalogowanym
    if not request.user.is_authenticated:
        return render(request, 'parts/parish_request_access.html', {'error_user': True})

    try:
        parish = Parish.objects.get(pk=parish_id)
    except Parish.DoesNotExist:
        return render(request, 'parts/parish_request_access.html', {'error_parish': True})

    try:
        parish_user = ParishUser.objects.get(user=request.user, parish=parish)
    except ParishUser.DoesNotExist:
        parish_user = ParishUser()
        parish_user.user = request.user
        parish_user.parish = parish

    if parish_user.manager_request:
        return render(request, 'parts/parish_request_access.html', {'error_already_clicked': True})
    else:
        parish_user.manager_request = True
        parish_user.manager_request_date = datetime.utcnow()
        parish_user.save()

        # mail d admina
        subject = '[katalog] Prosba o dostep'
        url = 'https://katalog.projektpodlasie.pl/a/users'
        message = u'Prosba o dostep od %s %s.\n%s' % (request.user.first_name, request.user.last_name, url, )
        for stf in User.objects.filter(is_staff=True):
            send_mail(subject, message, 'info@parafie.k37.ovh', (stf.email,) )

    return render(request, 'parts/parish_request_access.html', {
        #'parish': parish,
        #'parish_user': parish_user
    })


def validation_required(request):
    return render(request, 'core/validation_required.html')

###############################################################################

def contact(request):
    return render(request, 'core/contact.html')


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


def __prepare_report(sorted_documents):
    all = {
        'b': [],
        'd': [],
        'm': [],
        'a': [],
        'zap': []
    }

    for document in sorted_documents:
        date_from = document.date_from
        date_to = document.date_to
        for attr in ['b', 'd', 'm', 'a', 'zap']:
            if getattr(document, 'type_%s' % attr):
                sizeof = len(all[attr])
                if sizeof > 0:
                    last = all[attr][sizeof-1]
                    if last[1] >= date_from-1:
                        # nakladaja sie
                        all[attr][sizeof-1] = (all[attr][-1:][0][0], date_to)
                        continue
                all[attr].append((date_from, date_to))
    return all


def __prepare_report_yby(documents):
    all = {
        'b': {},
        'd': {},
        'm': {},
        'a': {},
        'zap': {}
    }
    
    for document in documents:
        date_from = document.date_from
        date_to = document.date_to
        for attr in ['b', 'd', 'm', 'a', 'zap']:
            if getattr(document, 'type_%s' % attr):
                for year in range(date_from, date_to+1):
                    if not year in all[attr].keys():
                        all[attr][year] = []
                    all[attr][year].append({
                        'year': year,
                        'copy_type': document.copy_type_str(),
                        'note': document.note,
                        'source': document.source.name,
                        'source_group': document.source.group
                    })
    return all


def _load_root_items():
    data ={}
    data['countries'] = Country.objects.all().filter(public=True)
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
        'geo_lng': x.geo_lng,
        'any_issues': x.any_issues()
    }, Parish.objects.filter(**args).order_by('place', 'name')))


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
