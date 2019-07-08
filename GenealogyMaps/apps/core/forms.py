
from django import forms

from .models import ParishSource, CourtBook


class ParishSourceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ParishSourceForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name in ('type_b', 'type_m', 'type_d', 'type_a', 'type_sum_only'):
                field.widget.attrs['class'] = 'form-check-input_'
            else:
                field.widget.attrs['class'] = 'form-control'
            if field_name in ('date_excepts', 'note'):
                field.widget.attrs['rows'] = '3'

    class Meta:
        model = ParishSource
        fields = ['type_b', 'type_d', 'type_m', 'type_a', 'type_sum_only', 'date_from', 'date_to', 'note', 'source', 'copy_type', ]

    error_css_class = 'is-invalid3'


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)


class CourtBookForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CourtBookForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            #if field_name in ('type_b', 'type_m', 'type_d', 'type_a', 'type_sum_only'):
            #    field.widget.attrs['class'] = 'form-check-input_'
            #else:
            #    field.widget.attrs['class'] = 'form-control'
            if field_name in ('owner_note', ):
                field.widget.attrs['rows'] = '3'
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = CourtBook
        fields = ['name', 'owner_note']

    error_css_class = 'is-invalid3'
