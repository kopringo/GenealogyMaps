
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext as _
from django.dispatch import receiver
from django.db.models import Q
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.

# https://pl.wikipedia.org/wiki/Zwi%C4%85zki_wyznaniowe_w_II_Rzeczypospolitej
RELIGION_TYPE__RC = 1
RELIGION_TYPE__SZ = 2
RELIGION_TYPE__WSCHODNI = 3
RELIGION_TYPE__MUZULMANSKI = 4
RELIGION_TYPE__EA = 5
RELIGION_TYPE__PRAWOSLAWNY = 6
RELIGION_TYPE__GK = 7
RELIGION_TYPE = (
    (RELIGION_TYPE__RC, 'Kościół rzymskokatolicki'),
    (RELIGION_TYPE__SZ, 'Żydowski Związek Wyznaniowy'),
    (RELIGION_TYPE__WSCHODNI, 'Wschodni Kościół Staroobrzędowy'),
    (RELIGION_TYPE__MUZULMANSKI, 'Muzułmański Związek Religijny'),
    (RELIGION_TYPE__EA, 'Kościół Ewangelicko-Augsburski'),
    (RELIGION_TYPE__PRAWOSLAWNY, 'Polski Kościół Prawosławny'),
    (RELIGION_TYPE__GK, 'Kościół Greckokatolicki')
)
RELIGION_TYPE_SHORT = {
    RELIGION_TYPE__RC: 'RK',
    RELIGION_TYPE__SZ: 'Ż',
    RELIGION_TYPE__WSCHODNI: 'W',
    RELIGION_TYPE__MUZULMANSKI: 'M',
    RELIGION_TYPE__EA: 'EA',
    RELIGION_TYPE__PRAWOSLAWNY: 'PR',
    RELIGION_TYPE__GK: 'GK',
}

PARISH_ACCESS__OPEN = 0
PARISH_ACCESS__CLOSED = 1
PARISH_ACCESS = (
    (PARISH_ACCESS__OPEN, 'Otwarty'),
    (PARISH_ACCESS__CLOSED, 'Zamknięty'),
)

COUNTRY_HP = (
    (1, 'I RP'),
    (2, 'II RP'),
    (3, 'III RP'),
    (4, 'RZ'),
)
def country_hp_to_name(number):
    for CHP in COUNTRY_HP:
        if number == CHP[0]:
            return CHP[1]
    return ''

def my_year_validator(value):
    if value < 1000 or value > 2100:
        raise ValidationError(
            _('%(value)s is not a correct year!'),
            params={'value': value},
        )


###############################################################################
# Lokalizacja
###############################################################################

class Country(models.Model):
    """
    Kraj
    """

    code = models.CharField(max_length=2, help_text='2 literowy kod kraju')
    name = models.CharField(max_length=32, help_text='Nazwa kraju')
    public = models.BooleanField(default=False)

    historical_period = models.IntegerField('Okres historyczny', default=1, choices=COUNTRY_HP, help_text='Kraje z dane okresu historycznego będą prezentowane wspólnie')
    
    description = models.TextField(blank=True, help_text='Opis na stronę główną')

    def get_provinces(self):
        return Province.objects.filter(country=self, public=True)

    def get_dioceses(self, religion=None):
        if religion is None:
            return Diocese.objects.filter(country=self, public=True)
        return Diocese.objects.filter(country=self, public=True, religion=religion)

    def __str__(self):
        return u'%d. %s (%s)' % (self.id, self.name, country_hp_to_name(self.historical_period))

    def name_with_period(self):
        return '{} ({})'.format(self.name, country_hp_to_name(self.historical_period))

    class Meta:
        verbose_name = 'Kraj'
        verbose_name_plural = 'Region - Kraje'#_("countries")


class Province(models.Model):
    """
    Województwo
    """

    country = models.ForeignKey(Country, help_text='Kraj', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=32, help_text='Nazwa województwa')
    short = models.CharField(max_length=2, blank=True)
    public = models.BooleanField(default=False)

    def county_number(self):
        return u'%s' % str(County.objects.filter(province=self).count())

    def parish_number(self):
        return u'%s' % str(Parish.objects.filter(province=self).count())

    def __unicode__(self):
        return '{} -> {}. {}'.format(self.country, self.id, self.name)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = 'Województwo'
        verbose_name_plural = 'Region - Województwa'#_("provinces")
        ordering = ['name']


class County(models.Model):
    """ Powiat """

    province = models.ForeignKey(Province, help_text='Województwo', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=32, help_text='Powiat')

    def parish_number(self):
        return u'%s' % str(Parish.objects.filter(county=self).count())

    def __str__(self):
        return u'%d. %s' % (self.id, self.name)

    class Meta:
        verbose_name = 'Powiat'
        verbose_name_plural = 'Region - Powiaty'
        ordering = ['name']


class Diocese(models.Model):
    """ Diecezja """

    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=64, help_text='Diecezja')
    short = models.CharField(max_length=3, blank=True)
    url = models.URLField(max_length=128, blank=True, null=True)
    public = models.BooleanField(default=False)

    religion = models.IntegerField(default=1, choices=RELIGION_TYPE)

    def deanery_number(self):
        return u'%s' % str(Deanery.objects.filter(diocese=self).count())

    def parish_number(self):
        return u'%s' % str(Parish.objects.filter(diocese=self).count())

    def __str__(self):
        return '{} -> {}. {}'.format(self.country, self.id, self.name)

    class Meta:
        verbose_name = 'Diecezja'
        verbose_name_plural = 'Region - Diecezje'#_("dioceses")
        ordering = ['name']


class Deanery(models.Model):
    """ Dekanat """

    diocese = models.ForeignKey(Diocese, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=64, help_text='Dekanat')
    url = models.URLField(max_length=128, blank=True)

    def __str__(self):
        return '{}. {}'.format(self.id, self.name)

    class Meta:
        verbose_name = 'Dekanat'
        verbose_name_plural = 'Region - Dekanaty'#"deaneries"
        ordering = ['name']


class ZiemiaIRP(models.Model):

    name = models.CharField(max_length=64, help_text='Nazwa ziemi')

    def __str__(self):
        return u'%d. %s' % (self.id, self.name)

    class Meta:
        verbose_name_plural = "ziemie I RP"

###############################################################################
# User
###############################################################################


class UserProfile(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=64, blank=True, help_text='Imię')
    lastname = models.CharField(max_length=64, blank=True, help_text='Nazwisko')
    full_access = models.BooleanField(default=False, help_text='Pełen dostęp do danych')

    parishes = models.TextField(blank=True, help_text='Parafie ktorymi interesuje sie uzytkownik')
    lastnames = models.TextField(blank=True, help_text='Nazwiska ktorymi interesuje sie uzytkownik')

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username


#@receiver(post_save, sender=User)
#def create_or_update_user_profile(sender, instance, created, **kwargs):
#    if created:
#        UserProfile.objects.create(user=instance)
#    instance.userprofile.save()

###############################################################################
# Refs
###############################################################################

DOCUMENT_SOURCE__FOR__AM = 1
DOCUMENT_SOURCE__FOR__COURT = 2
DOCUMENT_SOURCE__FOR = (
    (DOCUMENT_SOURCE__FOR__AM, 'Dokumenty metrykalne'),
    (DOCUMENT_SOURCE__FOR__COURT, 'Akta sądowe'),
)

SOURCE_GROUP__OTHER='Other'
SOURCE_GROUP = (
    ('AP', 'Archiwa Państwowe (PL)'),
    ('AD', 'Archiwa Kościelne (PL)'),
    ('PAR_LOC', 'Archiwum Parafialne - na miejscu'),
    ('PAR', 'Archiwum Parafialne - Inne'),

#    ('BIB', 'Biblioteki'),
#    ('USC', 'Urzędy Stanu Cywilnego'),
#    ('AP_UA', 'Archiwa Państwowe (UA)'),
#    ('AP_LT', 'Archiwa Państwowe (LT)'),
#    ('AP_BY', 'Archiwa Państwowe (BY)'),
#    ('AP_RU', 'Archiwa Państwowe (RU)'),
#    ('AP_LV', 'Archiwa Państwowe (LV)'),
#    ('AP_RO', 'Archiwa Państwowe (RO)'),
    
    ('A_Z', 'Archiwa Zagraniczne'),
    
    (SOURCE_GROUP__OTHER, 'Inne'),
)

DOCUMENT_GROUP__COPY_TYPE__NONE = 0
DOCUMENT_GROUP__COPY_TYPE__KSIEGA = 6
DOCUMENT_GROUP__COPY_TYPE = (
    (DOCUMENT_GROUP__COPY_TYPE__NONE, ''),
    (DOCUMENT_GROUP__COPY_TYPE__KSIEGA, 'Księga'),
    (4, 'Sumariusz'),
    (7, 'Reptularz'),
)
#    (99, '-------------------'),
#    (1, 'Oryginał'),
#    (2, 'Duplikat ASC / USC'),
#    (3, 'Odpis'),
#    (5, 'Kopia dekanalna'),


COURT_BOOK_TYPE = (
    ('grodzkie', 'Grodzkie'),
    ('ziemskie', 'Ziemskie'),
    ('podkomorskie', 'Podkomorskie'),
    ('biskupie', 'Biskupie'),
    ('bartne', 'Bartne'),
    ('wojtowskie', 'Wójtowskie'),
    ('radzieckie', 'Radzieckie'),
    ('lawnicze', 'Ławnicze'),
    ('kapicjana', 'Kapicjana'),
    ('inne', 'Inne'),
)

class SourceRef(models.Model):

    copy_type = models.IntegerField(default=DOCUMENT_GROUP__COPY_TYPE__KSIEGA, choices=DOCUMENT_GROUP__COPY_TYPE)
    note = models.TextField(blank=True, help_text='Notatka')
    date_created = models.DateTimeField(blank=True, null=True, help_text='Data utworzenia')
    date_modified = models.DateTimeField(blank=True, null=True, help_text='Data utworzenia')
    user = models.ForeignKey(User, null=True, help_text='Autor rekordu', on_delete=models.DO_NOTHING)

    def copy_type_str(self):
        for ct in DOCUMENT_GROUP__COPY_TYPE:
            if ct[0] == self.copy_type:
                return ct[1]
        return ''

    @classmethod
    def str_to_copy_type(cls, name):
        lower_name = name.lower()
        for ct in DOCUMENT_GROUP__COPY_TYPE:
            if ct[1].lower() == lower_name:
                return ct[0]
        return None

    class Meta:
        abstract = True

class Source(models.Model):

    name = models.CharField(max_length=64)
    short = models.CharField(max_length=16, blank=True)
    url = models.URLField(max_length=64, blank=True)

    group = models.CharField(max_length=32, blank=True, help_text='Grupa źródeł', choices=SOURCE_GROUP, default=SOURCE_GROUP__OTHER)
    note = models.TextField(blank=True)
    a_par_for_auto_import = models.BooleanField(default=False)

    # 
    country = models.ForeignKey(Country, null=True, on_delete=models.DO_NOTHING)
    place = models.CharField(max_length=32, help_text='Miejscowość', blank=True)
    address = models.CharField(max_length=32, help_text='Adres, ulica i numer', blank=True)
    geo_lat = models.FloatField(blank=True, null=True)
    geo_lng = models.FloatField(blank=True, null=True)

    def __str__(self):
        return u'%s' % (self.name)

    class Meta:
        verbose_name = 'Zbiór danych - źródło'
        verbose_name_plural = 'Zbiory danych - źródła'#_("countries")

###############################################################################
# Parafie
###############################################################################


class Parish(models.Model):

    # nazwa parafii
    name = models.CharField(max_length=32, help_text='Parafia pod wezwaniem')
    religion = models.IntegerField(default=1, choices=RELIGION_TYPE)
    year = models.IntegerField(blank=True, null=True, help_text='Data erygowania', validators=[my_year_validator])
    year_inexact = models.BooleanField(default=False, help_text='Czy data niedokładna')
    century = models.CharField(blank=True, null=True, max_length=8, help_text='Wiek powstania')
    access = models.IntegerField(default=0, choices=PARISH_ACCESS)
    visible = models.BooleanField(default=True, help_text='Czy parafia ma być widoczna na mapie/liście', db_index=True)

    # lokalizacja
    country = models.ForeignKey(Country, null=True, on_delete=models.DO_NOTHING)
    province = models.ForeignKey(Province, null=True, blank=True, on_delete=models.DO_NOTHING, help_text='Województwo (R3)')
    county = models.ForeignKey(County, null=True, blank=True, on_delete=models.DO_NOTHING, help_text='Powiat (R3)', limit_choices_to=Q(province__country__historical_period=3))
    place = models.CharField(max_length=32, help_text='Miejscowość')
    place2 = models.CharField(max_length=32, help_text='Miejscowość, nazwa historyczna', blank=True)
    postal_code = models.CharField(max_length=16, help_text='Kod pocztowy')
    postal_place = models.CharField(max_length=32, help_text='Poczta')
    address = models.CharField(max_length=64, help_text='Adres, ulica i numer', blank=True, null=True)

#    R1 966-1772
#    RZ 1795-1918
#    R2 1918-1939
#    R3 1945-2019

    county_r1 = models.ForeignKey(County, null=True, blank=True, on_delete=models.SET_NULL, help_text='Powiat w R1', related_name='county_r1', limit_choices_to=Q(province__country__historical_period=1))
    county_r2 = models.ForeignKey(County, null=True, blank=True, on_delete=models.SET_NULL, help_text='Powiat w R2', related_name='county_r2', limit_choices_to=Q(province__country__historical_period=2))
    county_rz = models.ForeignKey(County, null=True, blank=True, on_delete=models.SET_NULL, help_text='Powiat w RZ', related_name='county_rz', limit_choices_to=Q(province__country__historical_period=4))

    # lokalizacja
    geo_lat = models.FloatField(blank=True, null=True)
    geo_lng = models.FloatField(blank=True, null=True)
    geo_validated = models.BooleanField(default=False)
    not_exist_anymore = models.BooleanField(default=False, help_text='Parafia już nie istnieje')

    # podzial administracyjny koscielny
    diocese = models.ForeignKey(Diocese, null=True, blank=True, on_delete=models.DO_NOTHING, help_text='Diecezja')
    deanery = models.ForeignKey(Deanery, null=True, blank=True, on_delete=models.DO_NOTHING, help_text='Dekanat', limit_choices_to=Q(diocese__country__historical_period=3))

    deanery_r1 = models.ForeignKey(Deanery, null=True, blank=True, on_delete=models.DO_NOTHING, help_text='Dekanat w R1', related_name='deanery_r1', limit_choices_to=Q(diocese__country__historical_period=1))
    deanery_r2 = models.ForeignKey(Deanery, null=True, blank=True, on_delete=models.DO_NOTHING, help_text='Dekanat w R2', related_name='deanery_r2', limit_choices_to=Q(diocese__country__historical_period=2))
    deanery_rz = models.ForeignKey(Deanery, null=True, blank=True, on_delete=models.DO_NOTHING, help_text='Dekanat w RZ', related_name='deanery_rz', limit_choices_to=Q(diocese__country__historical_period=4))

    # podzial ziem I RP.
    ziemia_i_rp = models.ForeignKey(ZiemiaIRP, blank=True, null=True, on_delete=models.DO_NOTHING, help_text='Ziemia I RP')

    # kontakt
    phone = models.CharField(max_length=32, help_text=16, blank=True)
    link = models.URLField(blank=True)

    gen_id = models.IntegerField(unique=True, blank=True, null=True)
    szwa_id = models.CharField(blank=True, max_length=64)  # 53/1847/0
    fs_catalog_id = models.CharField(blank=True, max_length=64)
    partial_done = models.BooleanField(default=False, help_text='Częściowo wypełniona, tj. są księgi jakieś wpisane.')
    all_done = models.BooleanField(default=False, help_text='Oznacza parafię całkowicie uzuepłnioną (wg wiedzy opiekunów). To pole nadpisuje pole częściowego wypełnienia.')

    places = models.TextField(help_text='Lista miejscowości', blank=True)
    main_parish = models.ForeignKey('Parish', blank=True, null=True, on_delete=models.SET_NULL, related_name='main_parish2', \
                                    help_text='Parafia główna jeśli to jest filia')

    date_updated = models.DateTimeField(default=None, null=True, help_text='Data aktualizacji')

    slug = models.CharField(max_length=16, null=True, unique=True, help_text='Unikatowy losowy identyfikator parafii')

    def __str__(self):
        return u'%s. %s' % (str(self.id), self.name)

    def get_religion_description(self):
        try:
            return RELIGION_TYPE[self.religion-1][1]
        except:
            return ''

    def get_religion_short(self):
        try:
            return RELIGION_TYPE_SHORT[self.religion]
        except:
            return ''

    def refresh_summary(self, save_partial_done=False):
        # todo refresh summary

        # partial done
        self.partial_done = True
        self.save()

    def any_issues(self):
        diocese_str = ''
        deanery_str = ''
        geo_str = ''
        geo_str2 = ''
        missing_sth = ''
        not_exists = ''
        all_done = ''

        if not self.diocese_id:
            diocese_str = 'brak diecezji'
        if not self.deanery_id:
            deanery_str = 'brak dekanatu'
        if diocese_str != '' or deanery_str != '':
            missing_sth = '<span class="span-icon text-danger fa fa-exclamation-triangle" title="%s %s"></span>' % (diocese_str, deanery_str)

        # lokalizacja
        if (not self.geo_lat) or (not self.geo_lng):
            geo_str = '<span class="span-icon text-danger fa fa-map-marker" title="Brak współrzędnych"></span>'
        else:
            if self.geo_validated:
                geo_str = '<span class="span-icon text-success fa fa-map-marked" title="Współrzedne zatwierdzone"></span>'
            else:
                geo_str = '<span class="span-icon text-warning fa fa-map-marker" title="Współrzedne nie zatwierdzone"></span>'


        # nie istnieje
        if self.not_exist_anymore:
            not_exists = '<span class="span-icon text-danger fa fa-ban" title="Parafia nie istnieje obecnie."></span>'

        # wypelnienie
        if not self.partial_done and not self.all_done:
            all_done = '<span class="span-icon text-secondary fa fa-circle-o" title="Parafia nieuzupełniona"></span>'
        else:
            if self.partial_done:
                all_done = '<span class="span-icon text-warning fa fa-circle-o" title="Parafia w trakcie uzupełniania"></span>'
            if self.all_done:
                all_done = '<span class="span-icon text-success fa fa-check-circle" title="Parafia w pełni uzupełniona"></span>'
        if (self.year is not None) and (self.year >= 1946):
            all_done = '<span class="span-icon text-success fa fa-check-circle" title="Parafia erygowana po 1946"></span>'

        return u'%s%s%s%s' % (all_done, geo_str, missing_sth, not_exists)

    def has_user_manage_permission(self, user):

        # sprawdzenie czy admin
        if not user.is_authenticated:
            return False
        if user.is_staff:
            return True

        # przypisanie parafii do usera
        try:
            parish_user = ParishUser.objects.get(user=user, parish=self)
            if parish_user.manager:
                return True
        except:
            pass

        # spr. przypisanie do powiatu
        try:
            group_name = 'county_{}'.format(str(self.county_id))
            group = Group.objects.get(name=group_name)
            if user in group.user_set.all():
                return True
        except:
            pass

        return False

    class Meta:
        verbose_name = 'Parafia'
        verbose_name_plural = 'Parafie'


class ParishLocations(Parish):
    class Meta:
        proxy = True
        verbose_name = 'Parafia - lokalizacja'
        verbose_name_plural = 'Parafie - lokalizacje'


class ParishUser(models.Model):
    parish = models.ForeignKey(Parish, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    note = models.TextField(blank=True)

    favorite = models.BooleanField(default=False, help_text='Czy parafia nalezy do ulubionych usera')
    manager = models.BooleanField(default=False, help_text='Czy mamy uprawnienia do zarządzania parafią')
    manager_request = models.BooleanField(default=False, help_text='Zadanie dostepu do zarzadzania parafia')
    manager_request_date = models.DateTimeField(blank=True, null=True, help_text='')

    class Meta:
        unique_together = ('parish', 'user', )


class ParishPlace(models.Model):

    PLACE_TYPE__OTHER = 0
    PLACE_TYPE__CEMETERY = 1
    PLACE_TYPE = (
        (PLACE_TYPE__OTHER, 'Inny'),
        (PLACE_TYPE__CEMETERY, 'Cmentarz'),
    )

    parish = models.ForeignKey(Parish, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=32, help_text='Opis')
    type = models.IntegerField(choices=PLACE_TYPE, default=1)
    geo_lat = models.FloatField(blank=True)
    geo_lng = models.FloatField(blank=True)
    existing = models.BooleanField(default=True, help_text='Obiekt istniejący')


class ParishComment(models.Model):
    parish = models.ForeignKey(Parish, on_delete=models.DO_NOTHING, help_text='Parafia')
    data = models.TextField(blank=True, help_text='Tresc komentarza')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, help_text='Autor komentarza')
    date_created = models.DateTimeField(blank=True, null=True, help_text='Data utworzenia')
    visible = models.BooleanField(default=True, help_text='Widocznosc komentarza')


class ParishSource(SourceRef):

    parish = models.ForeignKey(Parish, on_delete=models.DO_NOTHING, help_text='Parafia', related_name='parish')
    source = models.ForeignKey(Source, on_delete=models.DO_NOTHING)
    source_parish = models.ForeignKey(Parish, blank=True, null=True, on_delete=models.SET_NULL, related_name='source_parish')
    
    #type = models.IntegerField(choices=DOCUMENT_GROUP__TYPE, help_text='Typ dokumentów', default=0)
    type_b = models.BooleanField(default=False, help_text='Akty urodzenia')
    type_d = models.BooleanField(default=False, help_text='Akty zgonu')
    type_m = models.BooleanField(default=False, help_text='Akty małżeństwa')
    type_a = models.BooleanField(default=False, help_text='Alegaty')
    type_zap = models.BooleanField(default=False, help_text='Zapowiedzi')
    type_sum_only = models.BooleanField(default=False, help_text='Dostępny tylko sumariusz')

    date_from = models.IntegerField(help_text='Zakres dat: od roku', default=1800, validators=[my_year_validator])
    date_to = models.IntegerField(help_text='Zakres dat: do roku', default=1900, validators=[my_year_validator])

    meta_record = models.BooleanField(default=False, help_text='Meta rekord oznacza serię ksiąg parafialnych w podanym zakresie')

#    def __str__(self):
#        return u'%s' % str(self.id)
#        #return u'%s (%s - %s)' % (self.parish, str(self.date_from), str(self.date_to))

    def id_with_dates(self):
        return u'%d. %d-%d' % (self.id, self.date_from, self.date_to)

    class Meta:
        verbose_name = 'Parafia - Zbiór danych'
        verbose_name_plural = 'Parafie - zbiory danych'#_("countries")


class ParishSourceExt(models.Model):

    parish = models.ForeignKey(Parish, on_delete=models.DO_NOTHING, help_text='Parafia')

    name = models.CharField(max_length=32, help_text='Nazwa grupy dokumentów', blank=True)
    url = models.URLField(blank=True, help_text='Adres url pod którym dokumenty są dostępne')


class ParishIndexSource(models.Model):

    PARISH_INDEX_SOURCE__TEST = 0
    PARISH_INDEX_SOURCE__PP = 1
    PARISH_INDEX_SOURCE = (
        (PARISH_INDEX_SOURCE__TEST, 'Test'),
        (PARISH_INDEX_SOURCE__PP, 'Projekt Podlasie'),
    )

    parish = models.ForeignKey(Parish, on_delete=models.DO_NOTHING, help_text='Parafia')
    project = models.IntegerField(default=0, choices=PARISH_INDEX_SOURCE)
    url = models.URLField(blank=True, help_text='Adres informacji o indexach')

    checked_date = models.DateTimeField(blank=True, null=True)
    raw_data = models.TextField(blank=True)

    def project_name(self):

        return ParishIndexSource.PARISH_INDEX_SOURCE[self.project][1]


###############################################################################
# Ksiegi sadowe
###############################################################################

class CourtOffice(models.Model):

    name = models.CharField(max_length=32, help_text='Nazwa kancelarii')

    country = models.ForeignKey(Country, null=True, on_delete=models.DO_NOTHING)
    province = models.ForeignKey(Province, null=True, on_delete=models.DO_NOTHING, help_text='Województwo')
    county = models.ForeignKey(County, null=True, help_text='Powiat', on_delete=models.DO_NOTHING)
    place = models.CharField(max_length=32, help_text='Miejscowość', blank=True)
    address = models.CharField(max_length=32, help_text='Adres, ulica i numer', blank=True)

    geo_lat = models.FloatField(blank=True, null=True)
    geo_lng = models.FloatField(blank=True, null=True)

    # podzial ziem I RP.
    ziemia_i_rp = models.ForeignKey(ZiemiaIRP, blank=True, null=True, on_delete=models.DO_NOTHING, help_text='Ziemia I RP')

    #
    # wiek_od
    # wiek_do
    # notes

    def book_number(self):
        return u'%s' % str(CourtBook.objects.filter(office=self).count())

    def __str__(self):
        return u'%s' % (self.name)

    class Meta:
        verbose_name = 'Kancelaria'
        verbose_name_plural = 'Kancelarie'


class CourtBook(models.Model):

    name = models.CharField(max_length=64, help_text='Nazwa księgi', blank=True)
    office = models.ForeignKey(CourtOffice, on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=32, blank=True, choices=COURT_BOOK_TYPE)

    #date_from = models.IntegerField(help_text='Zakres dat: od roku', default=1800)
    #date_to = models.IntegerField(help_text='Zakres dat: do roku', default=1900)
    #zespol = models.CharField(max_length=64, blank=True)
    #sygnatura = models.CharField(max_length=64, blank=True)

    # autor rekordu
    owner = models.ForeignKey(User, null=True, help_text='Osoba dodająca księgę', on_delete=models.DO_NOTHING)
    owner_note = models.TextField(blank=True, help_text='Notatka')
    owner_date_created = models.DateTimeField(blank=True, null=True, help_text='Data dodania księgi')

    def __str__(self):
        return u'%s' % (self.name)

    class Meta:
        verbose_name = 'Księga sądowa'
        verbose_name_plural = 'Księgi sądowe'


class CourtBookSource(SourceRef):

    book = models.ForeignKey(CourtBook, on_delete=models.DO_NOTHING, help_text='Księga')
    source = models.ForeignKey(Source, on_delete=models.DO_NOTHING)
    
    # 
    zespol = models.CharField(max_length=64, blank=True)
    sygnatura = models.CharField(max_length=64, blank=True)

    date_from = models.IntegerField(help_text='Zakres dat: od roku', default=1800)
    date_to = models.IntegerField(help_text='Zakres dat: do roku', default=1900)

    def __str__(self):
        return u'%s' % (self.book, )

    def id_with_dates(self):
        return u'%d. %d-%d' % (self.id, self.date_from, self.date_to)

    class Meta:
        verbose_name = 'Księga sądowa - zbiór danych'
        verbose_name_plural = 'Księgi sądowe - zbiory danych'#_("countries")
    

# 
def save_parish(sender, instance, **kwargs):
    try:
        if isinstance(instance, Parish):
            instance.date_updated = timezone.now()
            instance.save()
        else:
            instance.parish.date_updated = timezone.now()
            instance.parish.save()
    except:
        pass

#post_save.connect(save_parish, sender=Parish)
#post_save.connect(save_parish, sender=ParishPlace)
#post_save.connect(save_parish, sender=ParishComment)
#post_save.connect(save_parish, sender=ParishSource)
#post_save.connect(save_parish, sender=ParishSourceExt)

"""
class ParishRawData(models.Model):
    # Surowe dane na temat parafii

    
    parish = models.ForeignKey(Parish, blank=True, null=True, on_delete=models.DO_NOTHING)
    parish_source = models.ForeignKey('Source', blank=True, null=True, on_delete=models.DO_NOTHING)
    data_source = models.CharField(max_length=16, blank=True)
    data_key = models.CharField(max_length=64)
    data = models.TextField(blank=True)

    class Meta:
        unique_together = (('data_source', 'data_key'), )
        verbose_name = 'Parafia - dane surowe'
        verbose_name_plural = 'Parafie - dane surowe'  # "parishes"
"""
