from django.shortcuts import render, redirect


def names(request):

    data = {}


    return render(request, 'core/tools/names.html', data)
