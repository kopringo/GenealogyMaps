from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User

import numpy as np

# Create your views here.
from .models import Parish, Diocese, Province, County, Deanery, Source, ParishSource, ParishUser, Country, SOURCE_GROUP, ParishIndexSource
from .forms import ParishSourceForm, ParishEditForm, ParishMessageForm
from .decorators import group_required

def __prepare_common_params():
    return {
        'main_menu': 'churches',
        'body_map': True
    }


def parish(request, parish_id):
    """ Widok parafii """
    try:
        parish = Parish.objects.get(pk=parish_id)
    except Parish.DoesNotExist:
        return redirect('home') # '?error=doesnotexist'
    documents = ParishSource.objects.filter(parish=parish).order_by('date_from')
    documents_sorted = __prepare_report(documents)
    documents_yby = __prepare_report_yby(documents)

    documents_indexes = ParishIndexSource.objects.filter(parish=parish)

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
        'documents_indexes': documents_indexes,
        'manager': parish.has_user_manage_permission(request.user),
        'managers': ParishUser.objects.filter(parish=parish, manager=True),
        'parish_user': parish_user,
        'manager_exists': manager_exists,
        'subtitle': parish.place,
        'SOURCE_GROUP': SOURCE_GROUP,

        'limit_parish_on_the_map': '?lt=parish&lv={}'.format(parish_id)

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
    form = ParishMessageForm(initial={'title': '%s, %s' % (parish.name, parish.place)})

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

    parish_list = Parish.objects.filter(visible=True).values('id', 'name', 'geo_lat', 'geo_lng', 'province__id', 'county__id', 'place', 'address')

    limit_type = request.GET.get('lt', None)
    limit_value = request.GET.get('lv', '')
    limit_value = int(limit_value) if limit_value.isdigit() else None

    if (limit_type is not None) and (limit_value is not None):
        if limit_type == 'province':
            parish_list = parish_list.filter(province=limit_value)
        if limit_type == 'county':
            parish_list = parish_list.filter(county=limit_value)
        if limit_type == 'parish':
            try:
                parish = Parish.objects.get(pk=limit_value)
                parish_list = parish_list.filter(geo_lat__gt=parish.geo_lat-0.2, geo_lat__lt=parish.geo_lat+0.2,  geo_lng__gt=parish.geo_lng-0.2, geo_lng__lt=parish.geo_lng+0.2)
            except Exception as e:
                print(e)
                pass

    _items = list(parish_list)
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

        # hack, jesli wybieramy archiwum parafialne to ustawiamy na sztywno source jako wpis techniczny z bazy
        # i relacja idzie do parish
        if post.get('source_type', None) == 'PAR':
            par = True
            post['source'] = Source.objects.filter(group='PAR')[0].id

        # jesli wybieramy "parafia na miejscu" tj PAR_LOC to jw.
        if post.get('source_type', None) == 'PAR_LOC':
            post['source'] = Source.objects.filter(group='PAR_LOC')[0].id

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

                    # ostatni zakres z listy biore
                    last = all[attr][sizeof-1]

                    # jezeli istniejacy zakres konczy sie dalej niż nowy dokument zaczyna tzn. ze moga sie pokrywac
                    # pierwsze roczniki. nie bedzie przerwy, nie trzeba konczyc zakresu (koniecznie CONTINUE)
                    if last[1] >= date_from-1:

                        # nowy zakres musi sie jednak konczyc dalej, wtedy aktualizujemy date_to.
                        # to jest zabezpieczenie na wypadek zakresu ujetego w calosci w istniejacym
                        if date_to > last[1]:
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
