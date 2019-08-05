from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

# https://pl.wikipedia.org/wiki/Zwi%C4%85zki_wyznaniowe_w_II_Rzeczypospolitej
RELIGION_TYPE__RC = 1
RELIGION_TYPE__SZ = 2
RELIGION_TYPE__WSCHODNI = 3
RELIGION_TYPE__MUZULMANSKI = 4
RELIGION_TYPE__EA = 5
RELIGION_TYPE__PRAWOSLAWNY = 6
RELIGION_TYPE = (
    (RELIGION_TYPE__RC, 'Kościół rzymskokatolicki'),
    (RELIGION_TYPE__SZ, 'Żydowski Związek Wyznaniowy'),
    (RELIGION_TYPE__WSCHODNI, 'Wschodni Kościół Staroobrzędowy'),
    (RELIGION_TYPE__MUZULMANSKI, 'Muzułmański Związek Religijny'),
    (RELIGION_TYPE__EA, 'Kościół Ewangelicko-Augsburski'),
    (RELIGION_TYPE__PRAWOSLAWNY, 'Polski Kościół Prawosławny')
)

PARISH_ACCESS__OPEN = 0
PARISH_ACCESS__CLOSED = 1
PARISH_ACCESS = (
    (PARISH_ACCESS__OPEN, 'Otwarty'),
    (PARISH_ACCESS__CLOSED, 'Zamknięty'),
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

    def get_provinces(self):
        return Province.objects.filter(country=self, public=True)

    def __str__(self):
        return u'%d. %s' % (self.id, self.name)

    class Meta:
        verbose_name = 'Kraj'
        verbose_name_plural = 'Kraje'#_("countries")


class Province(models.Model):
    """
    Województwo
    """

    country = models.ForeignKey(Country, help_text='Kraj', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=32, help_text='Nazwa województwa')
    short = models.CharField(max_length=2, blank=True)
    public = models.BooleanField(default=False)

    def county_number(self):
        return u'%s' % str(len(County.objects.filter(province=self)))

    def parish_number(self):
        return u'%s' % str(len(Parish.objects.filter(province=self)))

    def __unicode__(self):
        return u'<%s>' % (self.name)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = 'Województwo'
        verbose_name_plural = 'Region - Województwa'#_("provinces")


class County(models.Model):
    """ Powiat """

    province = models.ForeignKey(Province, help_text='Województwo', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=32, help_text='Powiat')

    def parish_number(self):
        return u'%s' % str(len(Parish.objects.filter(county=self)))

    def __str__(self):
        return u'%d. %s' % (self.id, self.name)

    class Meta:
        verbose_name = 'Powiat'
        verbose_name_plural = 'Region - Powiaty'


class Diocese(models.Model):
    """ Diecezja """

    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=64, help_text='Diecezja')
    short = models.CharField(max_length=3, blank=True)
    url = models.URLField(max_length=128, blank=True, null=True)
    public = models.BooleanField(default=False)

    def deanery_number(self):
        return u'%s' % str(len(Deanery.objects.filter(diocese=self)))

    def parish_number(self):
        return u'%s' % str(len(Parish.objects.filter(diocese=self)))

    def __str__(self):
        return u'%d. %s' % (self.id, self.name)

    class Meta:
        verbose_name = 'Diecezja'
        verbose_name_plural = 'Region - Diecezje'#_("dioceses")


class Deanery(models.Model):
    """ Dekanat """

    diocese = models.ForeignKey(Diocese, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=64, help_text='Dekanat')
    url = models.URLField(max_length=128, blank=True)

    def __str__(self):
        return u'%d. %s' % (self.id, self.name)

    class Meta:
        verbose_name = 'Dekanat'
        verbose_name_plural = 'Region - Dekanaty'#"deaneries"


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

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()

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
    ('AP', 'Archiwum Państwowe - PL'),
    ('AD', 'Archiwum Diecezjalne - PL'),
    ('PAR', 'Archiwum Parafialne'),
    (SOURCE_GROUP__OTHER, 'Inne'),
)

DOCUMENT_GROUP__COPY_TYPE = (
    (1, 'Oryginał'),
    (2, 'Duplikat ASC / USC'),
    #(3, 'Odpis'),
    (5, 'Kopia dekanalna'),
    (4, 'Sumariusz'),
)

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

    copy_type = models.IntegerField(default=1, choices=DOCUMENT_GROUP__COPY_TYPE)
    note = models.TextField(blank=True, help_text='Notatka')
    date_created = models.DateTimeField(blank=True, null=True, help_text='Data utworzenia')
    date_modified = models.DateTimeField(blank=True, null=True, help_text='Data utworzenia')
    user = models.ForeignKey(User, null=True, help_text='Autor rekordu', on_delete=models.DO_NOTHING)

    class Meta:
        abstract = True

class Source(models.Model):

    name = models.CharField(max_length=64)
    short = models.CharField(max_length=16, blank=True)
    url = models.URLField(max_length=64, blank=True)

    group = models.CharField(max_length=32, blank=True, help_text='Grupa źródeł', choices=SOURCE_GROUP, default=SOURCE_GROUP__OTHER)
    parish = models.ForeignKey('Parish', blank=True, null=True, on_delete=models.SET_NULL)
    note = models.TextField(blank=True)

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
    year = models.IntegerField(blank=True, null=True, help_text='Data erygowania')
    access = models.IntegerField(default=0, choices=PARISH_ACCESS)

    # lokalizacja
    country = models.ForeignKey(Country, null=True, on_delete=models.DO_NOTHING)
    province = models.ForeignKey(Province, null=True, on_delete=models.DO_NOTHING, help_text='Województwo')
    county = models.ForeignKey(County, help_text='Powiat', on_delete=models.DO_NOTHING)
    place = models.CharField(max_length=32, help_text='Miejscowość')
    place2 = models.CharField(max_length=32, help_text='Miejscowość, nazwa historyczna', blank=True)
    postal_code = models.CharField(max_length=16, help_text='Kod pocztowy')
    postal_place = models.CharField(max_length=32, help_text='Poczta')
    address = models.CharField(max_length=32, help_text='Adres, ulica i numer')

    # lokalizacja
    geo_lat = models.FloatField(blank=True, null=True)
    geo_lng = models.FloatField(blank=True, null=True)
    geo_validated = models.BooleanField(default=False)
    not_exist_anymore = models.BooleanField(default=False, help_text='Parafia już nie istnieje')

    # podzial administracyjny koscielny
    diocese = models.ForeignKey(Diocese, null=True, blank=True, on_delete=models.DO_NOTHING, help_text='Diecezja')
    deanery = models.ForeignKey(Deanery, null=True, blank=True, on_delete=models.DO_NOTHING, help_text='Dekanat')

    # podzial ziem I RP.
    ziemia_i_rp = models.ForeignKey(ZiemiaIRP, blank=True, null=True, on_delete=models.DO_NOTHING, help_text='Ziemia I RP')

    # kontakt
    phone = models.CharField(max_length=32, help_text=16, blank=True)
    link = models.URLField(blank=True)

    gen_id = models.IntegerField(unique=True, blank=True, null=True)
    szwa_id = models.CharField(blank=True, max_length=64)  # 53/1847/0
    fs_catalog_id = models.CharField(blank=True, max_length=64)
    all_done = models.BooleanField(default=False, help_text='Oznacza parafię całkowicie uzuepłnioną (wg wiedzy opiekunów)')

    def __str__(self):
        return u'%d. %s' % (self.id, self.name)

    def get_religion_description(self):
        try:
            return RELIGION_TYPE[self.religion-1][1]
        except:
            return ''

    def refresh_summary(self):
        pass

    def any_issues(self):
        diocese_str = ''
        deanery_str = ''
        geo_str = ''
        geo_str2 = ''
        missing_sth = ''
        not_exists = ''
        all_done = ''

        if not self.diocese:
            diocese_str = 'brak diecezji'
        if not self.deanery:
            deanery_str = 'brak dekanatu'
        if diocese_str != '' or deanery_str != '':
            missing_sth = '<span class="text-danger fa fa-exclamation-triangle" title="%s %s"></span>' % (diocese_str, deanery_str)

        if (not self.geo_lat) or (not self.geo_lng):
            geo_str = '<span class="text-danger fa fa-map-marker" title="brak współrzędnych"></span>'
        if self.geo_validated:
            geo_str2 = '<span class="text-success fa fa-map-marker" title="współrzedne zatwierdzone"></span>'

        if self.not_exist_anymore:
            not_exists = '<span class="text-danger fa fa-ban" title="Parafia nie istnieje obecnie."></span>'

        if self.all_done:
            all_done = '<span class="text-success fa fa-check-circle" title="Parafia w pełni uzupełniona."></span>'

        return u'%s%s%s%s%s' % (missing_sth, geo_str, geo_str2, not_exists, all_done)

    def has_user_manage_permission(self, user):
        if not user.is_authenticated:
            return False
        if user.is_staff:
            return True
        try:
            parish_user = ParishUser.objects.get(user=user, parish=self)
            if parish_user.manager:
                return True
        except:
            pass
        return False

    class Meta:
        verbose_name = 'Parafia'
        verbose_name_plural = 'Parafie'#"parishes"


class ParishUser(models.Model):
    parish = models.ForeignKey(Parish, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    note = models.TextField(blank=True)

    favorite = models.BooleanField(default=False, help_text='Czy parafia nalezy do ulubionych usera')
    manager = models.BooleanField(default=False, help_text='Czy mamy uprawnienia do zarządzania parafią')
    manager_request = models.BooleanField(default=False, help_text='Zadanie dostepu do zarzadzania parafia')
    manager_request_date = models.DateTimeField(blank=True, null=True, help_text='')

    class Meta:
        unique_together = ('parish', 'user', )


class ParishPlace(models.Model):
    parish = models.ForeignKey(Parish, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=32)
    geo_lat = models.FloatField(blank=True)
    geo_lng = models.FloatField(blank=True)


class ParishComment(models.Model):
    parish = models.ForeignKey(Parish, on_delete=models.DO_NOTHING, help_text='Parafia')
    data = models.TextField(blank=True, help_text='Tresc komentarza')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, help_text='Autor komentarza')
    date_created = models.DateTimeField(blank=True, null=True, help_text='Data utworzenia')
    visible = models.BooleanField(default=True, help_text='Widocznosc komentarza')

class ParishSource(SourceRef):

    parish = models.ForeignKey(Parish, on_delete=models.DO_NOTHING, help_text='Parafia')
    source = models.ForeignKey(Source, on_delete=models.DO_NOTHING)
    
    #type = models.IntegerField(choices=DOCUMENT_GROUP__TYPE, help_text='Typ dokumentów', default=0)
    type_b = models.BooleanField(default=False, help_text='Akty urodzenia')
    type_d = models.BooleanField(default=False, help_text='Akty zgonu')
    type_m = models.BooleanField(default=False, help_text='Akty małżeństwa')
    type_a = models.BooleanField(default=False, help_text='Alegaty')
    type_zap = models.BooleanField(default=False, help_text='Zapowiedzi')
    type_sum_only = models.BooleanField(default=False, help_text='Dostępny tylko sumariusz')

    date_from = models.IntegerField(help_text='Zakres dat: od roku', default=1800)
    date_to = models.IntegerField(help_text='Zakres dat: do roku', default=1900)

    def __str__(self):
        return u'%s (%s - %s)' % (self.parish, str(self.date_from), str(self.date_to))

    def id_with_dates(self):
        return u'%d. %d-%d' % (self.id, self.date_from, self.date_to)

    class Meta:
        verbose_name = 'Parafia - Zbiór danych'
        verbose_name_plural = 'Parafie - zbiory danych'#_("countries")

class ParishSourceExt(models.Model):

    parish = models.ForeignKey(Parish, on_delete=models.DO_NOTHING, help_text='Parafia')

    name = models.CharField(max_length=32, help_text='Nazwa grupy dokumentów', blank=True)
    url = models.URLField(blank=True, help_text='Adres url pod którym dokumenty są dostępne')

###############################################################################
# Ksiegi sadowe
###############################################################################

class CourtOffice(models.Model):

    name = models.CharField(max_length=32, help_text='Nazwa kancelarii')

    country = models.ForeignKey(Country, null=True, on_delete=models.DO_NOTHING)

    # podzial ziem I RP.
    ziemia_i_rp = models.ForeignKey(ZiemiaIRP, blank=True, null=True, on_delete=models.DO_NOTHING, help_text='Ziemia I RP')

    def book_number(self):
        return u'%s' % str(len(CourtBook.objects.filter(office=self)))

    def __str__(self):
        return u'%s' % (self.name)

    class Meta:
        verbose_name = 'Kancelaria'
        verbose_name_plural = 'Kancelarie'

class CourtBook(models.Model):

    name = models.CharField(max_length=64, help_text='Nazwa księgi', blank=True)
    office = models.ForeignKey(CourtOffice, on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=32, blank=True, choices=COURT_BOOK_TYPE)

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
