from rest_framework import routers, serializers, viewsets

from .models import Parish


# Serializers define the API representation.
class ParishSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Parish
        fields = ('id', 'name', 'geo_lat', 'geo_lng')


# ViewSets define the view behavior.
class ParishViewSet(viewsets.ModelViewSet):
    queryset = Parish.objects.all()
    serializer_class = ParishSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'/parishes', ParishViewSet)