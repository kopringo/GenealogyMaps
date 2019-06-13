
from django import forms

from .models import Source


class SourceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SourceForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name in ('type_b', 'type_m', 'type_d', 'type_a'):
                field.widget.attrs['class'] = 'form-check-input_'
            else:
                field.widget.attrs['class'] = 'form-control'
            if field_name in ('date_excepts', 'note'):
                field.widget.attrs['rows'] = '3'

    class Meta:
        model = Source
        fields = ['type', 'type_b', 'type_d', 'type_m', 'type_a',     'name', 'url',  'date_from', 'date_to', 'date_excepts', 'note', 'source']

    error_css_class = 'is-invalid3'


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)