
from django import forms

from .models import ParishSource, CourtBook, Parish


class ParishMessageForm(forms.Form):
    title = forms.CharField(max_length=64, label='Tytuł wiadomości')
    body = forms.CharField(widget=forms.Textarea, label='Treść:')

    title.widget.attrs['class'] = 'form-control'
    body.widget.attrs['class'] = 'form-control'


class ParishEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ParishEditForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name not in ['not_exist_anymore', 'all_done', 'geo_validated']:
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Parish
        fields = [

            'name', 'religion', 'year', 'not_exist_anymore', 'all_done',

            'country',
            'province',
            'county',

            'diocese',
            'deanery',

            'ziemia_i_rp',

            'place',
            'place2',
            'postal_code',
            'postal_place',
            'address',

            'geo_lat',
            'geo_lng',
            'geo_validated',

            'places'
        ]


class ParishSourceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ParishSourceForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name in ('type_b', 'type_m', 'type_d', 'type_a', 'type_zap', 'type_sum_only'):
                field.widget.attrs['class'] = 'form-check-input_'
            else:
                field.widget.attrs['class'] = 'form-control'
            if field_name in ('date_excepts', 'note'):
                field.widget.attrs['rows'] = '3'

    class Meta:
        model = ParishSource
        fields = ['type_b', 'type_d', 'type_m', 'type_a', 'type_zap', 'type_sum_only', 'date_from', 'date_to', 'note', 'source', 'copy_type', ]

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
