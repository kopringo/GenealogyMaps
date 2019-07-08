from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime
import json

import numpy as np

# Create your views here.
from .models import Parish, Diocese, Province, County, Deanery, Source, ParishSource, CourtOffice, CourtBook, CourtBookSource
from .forms import CourtBookForm

def __prepare_common_params():
    return {
        'main_menu': 'courts'
    }


@login_required
def index(request):

    data = __prepare_common_params()
    data['offices'] = CourtOffice.objects.all().order_by('name')

    return render(request, 'core/_courts/index.html', data)


@login_required
def office(request, o_id):

    data = __prepare_common_params()

    try:
        office = CourtOffice.objects.get(pk=o_id)
        data['office'] = office
        data['books'] = CourtBook.objects.filter(office=office).order_by('name')
    except CourtOffice.DoesNotExist:
        redirect('/courts?error=')

    return render(request, 'core/_courts/office.html', data)


@login_required
def book(request, b_id):
    data = __prepare_common_params()

    try:
        book = CourtBook.objects.get(pk=b_id)
    except CourtBook.DoesNotExist:
        redirect('/courts?error=')

    if request.POST:
        source_id = request.POST.get('source', None)
        try:
            source = Source.objects.get(pk=int(source_id))
        except:
            return JsonResponse({'success': False, 'reason': 'no source'})
        data = json.loads(request.POST.get('data', None))
        for row in data:

            if row[0] is None or row[1] is None:
                continue

            cbs = CourtBookSource()
            cbs.book = book
            cbs.zespol = row[0]
            cbs.sygnatura = row[1]
            cbs.date_from = row[2]
            cbs.date_to = row[3]
            if cbs.date_to is None:
                cbs.date_to = cbs.date_from
            cbs.note = row[4]
            if cbs.note is None:
                cbs.note = ''
            cbs.user = request.user
            cbs.date_created = datetime.utcnow()
            cbs.source = source
            cbs.save()

        return JsonResponse({'success': True})

    data['book'] = book
    data['sources'] = Source.objects.all().order_by('group', 'name')
    data['cb_sources'] = CourtBookSource.objects.filter(book=book).order_by('zespol', 'sygnatura')


    return render(request, 'core/_courts/book.html', data)

@login_required
def court_add_book(request, o_id):


    form = CourtBookForm()
    saved = False


    # pobranie kancelarii
    try:
        office = CourtOffice.objects.get(pk=o_id)
    except CourtOffice.DoesNotExist:
        return redirect('/courts?error=parish-not-exits')

    """
    # document group jesli edytujemy
    dg = request.GET.get('dg', request.POST.get('dg', None))
    document_group = None
    if dg is not None:
        try:
            document_group = ParishSource.objects.get(pk=dg, parish=parish)
            form = ParishSourceForm(instance=document_group)
        except ParishSource.DoesNotExist:
            pass
    """

    if request.method == 'POST':
        form = CourtBookForm(request.POST)

        if form.is_valid():
            court_book = form.save(commit=False)
            court_book.office = office
            court_book.owner = request.user
            court_book.owner_date_created = datetime.utcnow()
            court_book.save()

            saved = True

    return render(request, 'core/_courts/add_book.html', {'form': form, 'saved': saved, 'office': office})
