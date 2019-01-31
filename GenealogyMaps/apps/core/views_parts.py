from django.shortcuts import render

# Create your views here.
from .models import Parish, Diocese, Province, County, Deanery, DocumentGroup
from .forms import DocumentGroupForm


def root(request):
    data = {}
    data.update(_load_root_items())
    return render(request, 'parts/root.html', data)


def area(request):
    province_id = request.GET.get('province', None)
    county_id = request.GET.get('county', None)
    diocese_id = request.GET.get('diocese', None)
    deanary_id = request.GET.get('deanary', None)

    items = []
    group_obj = None
    group_type = None

    try:
        province = Province.objects.get(pk=province_id)
        items = list(map(lambda x: {'name': x.name, 'link': '/parts/area?county=%d' % x.id}, County.objects.filter(province=province)))
        group_type = 'province'
        group_obj = province
    except Province.DoesNotExist:
        pass

    try:
        county = County.objects.get(pk=county_id)
        items = list(map(lambda x: {'name': '%s, %s' % (x.place, x.name), 'link': '/parts/parish?id=%d' % x.id}, Parish.objects.filter(county=county)))
        group_type = 'county'
        group_obj = county
    except County.DoesNotExist:
        pass

    try:
        diocese = Diocese.objects.get(pk=diocese_id)
        items = list(map(lambda x: {'name': x.name, 'link': '/parts/area?deanary=%d' % x.id}, Deanery.objects.filter(diocese=diocese)))
        group_type = 'diocese'
        group_obj = diocese
    except Diocese.DoesNotExist:
        pass

    try:
        deanary = Deanery.objects.get(pk=deanary_id)
        items = list(map(lambda x: {'name': '%s, %s' % (x.place, x.name), 'link': '/parts/parish?id=%d' % x.id}, Parish.objects.filter(deanery=deanary)))
        group_type = 'deanary'
        group_obj = deanary
    except Deanery.DoesNotExist:
        pass

    if len(items) == 0:
        return root(request)

    return render(request, 'parts/area.html', {'items': items, 'group_type': group_type, 'group_obj': group_obj})


def parish(request):
    id = request.GET.get('id', None)
    parish = Parish.objects.get(pk=id)
    documents = DocumentGroup.objects.filter(parish=parish)
    #comments =
    return render(request, 'parts/parish.html', {'parish': parish, 'document_groups': documents})


def document_add(request):
    form = DocumentGroupForm()
    saved = False

    parish_id = request.GET.get('parish', request.POST.get('parish', None))
    try:
        parish = Parish.objects.get(pk=parish_id)
    except:
        pass

    if request.method == 'POST':
        form = DocumentGroupForm(request.POST)

        if form.is_valid():
            document_group = form.save(commit=False)
            document_group.parish = parish
            document_group.user = request.user
            document_group.save()

            parish.refresh_summary()

            saved = True

    return render(request, 'parts/document_add.html', {'form': form, 'saved': saved, 'parish': parish})


def _load_root_items():

    data = {
        'provinces': [],
        'dioceses': []
    }

    data['provinces'] = Province.objects.all().filter(public=True)
    data['dioceses'] = Diocese.objects.all().filter(public=True)

    return data
