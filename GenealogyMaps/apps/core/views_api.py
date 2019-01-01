
from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework import routers, serializers, viewsets, generics
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, AdminRenderer, BrowsableAPIRenderer

from .models import Parish, Diocese, Province


###############################################################################
# Serializers

class ParishSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Parish
        fields = ('id', 'name', 'geo_lat', 'geo_lng')


class ParishDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parish
        fields = ('id', 'name', 'year', 'country', 'province', 'county', 'place', 'postal_code', 'postal_place', 'address', 'diocese', 'deanery')


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ('id', 'name')


class ProvinceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ('id', 'name')


class DioceseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ('id', 'name')


class DioceseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ('id', 'name')


class MultiSerializerViewSet(viewsets.ModelViewSet):
    serializers = {
        'default': None,
    }

    def get_serializer_class(self):
        default_serializer = None
        if 'default' in self.serializers.keys():
            default_serializer = self.serializers['default']
        if default_serializer is None and 'list' in self.serializers.keys():
            default_serializer = self.serializers['list']
        print(self.action)
        return self.serializers.get(self.action, default_serializer)


###############################################################################
# ViewSets

class ParishViewSet(MultiSerializerViewSet):
    model = Parish
    queryset = Parish.objects.all()
    serializers = {
        'list': ParishSerializer,
        'retrieve': ParishDetailSerializer,
    }
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, AdminRenderer, TemplateHTMLRenderer)
    template_name = 'core/api/parish_detail.html'


class ProvinceViewSet(MultiSerializerViewSet):
    model = Province
    queryset = Province.objects.all()
    serializers = {
        'list': ProvinceSerializer,
        'retrieve': ProvinceDetailSerializer,
    }


class DioceseViewSet(MultiSerializerViewSet):
    model = Diocese
    queryset = Diocese.objects.all()
    serializers = {
        'list': DioceseSerializer,
        'retrieve': DioceseDetailSerializer,
    }

"""
def parishes__get(request):
    data = {
        'parishes': list(Parish.objects.values('id', 'name', 'geo_lat', 'geo_lng').all()[0:2000])
    }
    response = JsonResponse(data)
    return response
"""
