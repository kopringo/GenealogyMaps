
from django.forms import ModelForm

from .models import DocumentGroup


class DocumentGroupForm(ModelForm):
    class Meta:
        model = DocumentGroup
        fields = ['name', 'url', 'type', 'type_b', 'type_d', 'type_m', 'type_a', 'date_from', 'date_to', 'date_excepts', 'note']
