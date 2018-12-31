
from django.urls import path, re_path
from django.conf.urls import url, include

from rest_framework import routers, serializers, viewsets, generics
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, AdminRenderer, BrowsableAPIRenderer

from .models import Parish


# Serializers define the API representation.
class ParishSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Parish
        fields = ('id', 'name', 'geo_lat', 'geo_lng')


class ParishDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parish
        fields = ('id', 'name', 'year', 'country', 'province', 'county', 'place', 'postal_code', 'postal_place', 'address', 'diocese', 'deanery')


class ParishList(generics.ListAPIView):
    queryset = Parish.objects.all()
    serializer_class = ParishSerializer

    """
    def get_queryset(self):
        username = self.kwargs['username']
        return Purchase.objects.filter(purchaser__username=username)
    """


class ParishDetails(generics.RetrieveAPIView):
    queryset = Parish.objects.all()
    serializer_class = ParishDetailSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, AdminRenderer, TemplateHTMLRenderer)
    template_name = 'core/api/parish_detail.html'

# Routers provide an easy way of automatically determining the URL conf.
#router = routers.DefaultRouter()
#router.register(r'/parishes', ParishList.as_view())
urlpatterns = [
    re_path(r'^parishes/$', ParishList.as_view()),
    path('parishes/<int:pk>/', ParishDetails.as_view()),
]
