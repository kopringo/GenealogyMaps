
from django.shortcuts import render
from django.http import JsonResponse

import os
from django.urls import reverse

from rest_framework.response import Response
from rest_framework import routers, serializers, viewsets, generics, relations
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, AdminRenderer, BrowsableAPIRenderer
from rest_framework.decorators import action

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

    def to_representation(self, instance):
        """Convert `username` to lowercase."""
        ret = super().to_representation(instance)
        ret['diocese'] = {
            'name': instance.diocese.name,
            'id': instance.diocese.id,
            #'uri': serializers.HyperlinkedIdentityField(
            #            view_name='diocese',
            #            lookup_field='id',
            #        ).to_representation(instance.diocese)
        }
        ret['deanery'] = {
            'name': instance.deanery.name,
            'id': instance.deanery.id,
        }
        ret['country'] = {
            'name': instance.country.name,
            'id': instance.country.id,
        }
        ret['province'] = {
            'name': instance.province.name,
            'id': instance.province.id,
        }
        ret['county'] = {
            'name': instance.county.name,
            'id': instance.county.id,
        }
        ret['links'] = {
            'places': '%s://%s/api2/parishes/%d/places/' % (os.environ.get('HTTP_PROTOCOL', ''), os.environ.get('HTTP_HOST', ''), instance.id),
            'documents': '%s://%s/api2/parishes/%d/documents/' % (os.environ.get('HTTP_PROTOCOL', ''), os.environ.get('HTTP_HOST', ''), instance.id),
            'comments': '%s://%s/api2/parishes/%d/comments/' % (os.environ.get('HTTP_PROTOCOL', ''), os.environ.get('HTTP_HOST', ''), instance.id)

        }
        return ret


class ProvinceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Province
        fields = ('id', 'name')


class ProvinceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ('id', 'name')


class DioceseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diocese
        fields = ('id', 'name')


class DioceseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diocese
        fields = ('id', 'name')


class MultiSerializerViewSet(viewsets.ReadOnlyModelViewSet):
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

    @action(detail=True, methods=['get'])
    def documents(self, request, pk=None):
        return Response({}, template_name='core/api/parish_detail_documents.html')

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        return Response({}, template_name='core/api/parish_detail_comments.html')


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

    @action(detail=True, methods=['get'])
    def deaneries(self, request, pk=None):
        province = self.get_object()
        """
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        """
        return Response({'status': 'password set'})

"""
def parishes__get(request):
    data = {
        'parishes': list(Parish.objects.values('id', 'name', 'geo_lat', 'geo_lng').all()[0:2000])
    }
    response = JsonResponse(data)
    return response
"""
