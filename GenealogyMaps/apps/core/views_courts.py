from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime

import numpy as np

# Create your views here.
from .models import Parish, Diocese, Province, County, Deanery, Source, ParishSource, CourtOffice, CourtBook, CourtBookSource

@login_required
def index(request):

    data = {}
    data['offices'] = CourtOffice.objects.all()

    return render(request, 'core/_courts/index.html', data)

@login_required
def office(request, o_id):
    data = {}

    try:
        office = CourtOffice.objects.get(pk=o_id)
        data['office'] = office
        data['books'] = CourtBook.objects.filter(office=office)
    except CourtOffice.DoesNotExist:
        redirect('/courts?error=')

    return render(request, 'core/_courts/office.html', data)

@login_required
def book(request, b_id):
    data = {}

    try:
        book = CourtBook.objects.get(pk=b_id)
        data['book'] = book
        data['sources'] = CourtBookSource.objects.filter(book=book)
    except CourtBook.DoesNotExist:
        redirect('/courts?error=')

    return render(request, 'core/_courts/book.html', data)