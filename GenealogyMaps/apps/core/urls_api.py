
from django.urls import path, re_path
from django.shortcuts import get_object_or_404
from django.conf.urls import url, include

from rest_framework.response import Response
from rest_framework import routers, serializers, viewsets, generics
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, AdminRenderer, BrowsableAPIRenderer

from .views_api import ParishViewSet, ProvinceViewSet, DioceseViewSet

from .models import Parish

"""
class ParishDetails(generics.RetrieveAPIView):
    queryset = Parish.objects.all()
    serializer_class = ParishDetailSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, AdminRenderer, TemplateHTMLRenderer)
    template_name = 'core/api/parish_detail.html'

    def get22(self, request, pk):
        obj = get_object_or_404(Parish, pk=pk)
        serializer = ParishDetailSerializer(obj)
        #serializer = {}
        return Response({'serializer': serializer.data})#, 'obj': obj})
"""

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'parishes', ParishViewSet)
router.register(r'provinces', ProvinceViewSet)
router.register(r'dioceses', DioceseViewSet)

"""
urlpatterns = [
    re_path(r'^parishes/$', ParishList.as_view()),
    path('parishes/<int:pk>/', ParishDetails.as_view()),
    path('', include(router.urls)),
]
"""
