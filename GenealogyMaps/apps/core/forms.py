
from django.forms import ModelForm

from .models import DocumentGroup


class DocumentGroupForm(ModelForm):
    class Meta:
        model = DocumentGroup
        fields = ['name', 'url', ]