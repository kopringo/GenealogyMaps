
from django import forms

from .models import ParishSource, CourtBook, Parish, ParishPlace, ParishSourceExt


class ParishMessageForm(forms.Form):
    title = forms.CharField(max_length=64, label='Tytuł wiadomości')
    body = forms.CharField(widget=forms.Textarea, label='Treść:')

    title.widget.attrs['class'] = 'form-control'
    body.widget.attrs['class'] = 'form-control'



class ParishEditBasicForm(forms.ModelForm):
    pass

class ParishEditPeriodsForm(forms.ModelForm):
    pass

class ParishEditGeoForm:
    pass


class ParishEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ParishEditForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name not in ['not_exist_anymore', 'all_done', 'geo_validated']:
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Parish
        fields = [

            'name', 'religion', 'year', 'century', 'not_exist_anymore', 'all_done',

            'country',
            'province',
            'county',

            'diocese',
            'deanery',

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


class ParishEditForm2(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ParishEditForm2, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name not in ['not_exist_anymore', 'all_done', 'geo_validated']:
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Parish
        fields = [

            'county_r2',
            'county_r1',
            'county_rz',
            'ziemia_i_rp',

        ]


class ParishPlaceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ParishPlaceForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ParishPlace
        fields = ['name', 'note', 'type', 'geo_lat', 'geo_lng', 'existing', ]


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

    def clean(self):
        cleaned_data = super(ParishSourceForm, self).clean()
        if not cleaned_data['type_b'] and \
           not cleaned_data['type_m'] and \
           not cleaned_data['type_d'] and \
           not cleaned_data['type_a'] and \
           not cleaned_data['type_zap']:
            raise forms.ValidationError('Jeden typ dokumentu musi byc wybrany', code='type_all')
        
        date_from = int(cleaned_data['date_from'])
        date_to = int(cleaned_data['date_to'])
        if date_from > date_to:
            self.add_error('date_from', 'Odwrócony zakres dat')
        
        return cleaned_data

    class Meta:
        model = ParishSource
        fields = ['type_b', 'type_d', 'type_m', 'type_a', 'type_zap', 'type_sum_only', 'date_from', 'date_to', 'note', 'source', 'copy_type', ]

    error_css_class = 'is-invalid3'


class ParishSourceExtForm(forms.ModelForm):
    class Meta:
        model = ParishSourceExt
        fields = ['name', 'url']


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
