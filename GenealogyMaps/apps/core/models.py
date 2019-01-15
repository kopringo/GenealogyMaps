from django.db import models
from django.contrib.auth.models import User

# Create your models here.

RELIGION_TYPE__RC = 1
RELIGION_TYPE = {
    (RELIGION_TYPE__RC, 'Kościół rzymskokatolicki'),
}

PARISH_ACCESS__OPEN = 0
PARISH_ACCESS__CLOSED = 1
PARISH_ACCESS = (
    (PARISH_ACCESS__OPEN, 'Otwarty'),
    (PARISH_ACCESS__CLOSED, 'Zamknięty'),
)


class Country(models.Model):
    """
    Kraj
    """

    code = models.CharField(max_length=2, help_text='2 literowy kod kraju')
    name = models.CharField(max_length=32, help_text='Nazwa kraju')

    def __str__(self):
        return u'%d. %s' % (self.id, self.name)

    class Meta:
        verbose_name_plural = "countries"


class Province(models.Model):
    """
    Województwo
    """

    country = models.ForeignKey(Country, help_text='Kraj', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=32, help_text='Nazwa województwa')
    short = models.CharField(max_length=2, blank=True)

    def __unicode__(self):
        return u'<%s>[%s]' % (self.name, self.country)

    def __str__(self):
        return self.__unicode__()


class County(models.Model):
    """
    Powiat
    """

    province = models.ForeignKey(Province, help_text='Województwo', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=32, help_text='Powiat')

    def __str__(self):
        return u'%d. %s' % (self.id, self.name)


class Diocese(models.Model):

    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=64, help_text='Diecezja')
    short = models.CharField(max_length=3, blank=True)
    url = models.URLField(max_length=128, blank=True, null=True)

    def __str__(self):
        return u'%d. %s' % (self.id, self.name)


class Deanery(models.Model):

    diocese = models.ForeignKey(Diocese, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=64, help_text='Dekanat')
    url = models.URLField(max_length=128, blank=True)

    def __str__(self):
        return u'%d. %s' % (self.id, self.name)

    class Meta:
        verbose_name_plural = "deaneries"



class ZiemiaIRP(models.Model):

    name = models.CharField(max_length=64, help_text='Nazwa ziemi')

    def __str__(self):
        return u'%d. %s' % (self.id, self.name)

    class Meta:
        verbose_name_plural = "ziemie I RP"


class Parish(models.Model):

    # nazwa parafii
    name = models.CharField(max_length=32, help_text='Parafia pod wezwaniem')
    religion = models.IntegerField(default=1, choices=RELIGION_TYPE)
    year = models.IntegerField(blank=True, help_text='Data erygowania')
    access = models.IntegerField(default=0, choices=PARISH_ACCESS)

    # lokalizacja
    country = models.ForeignKey(Country, null=True, on_delete=models.DO_NOTHING)
    province = models.ForeignKey(Province, null=True, on_delete=models.DO_NOTHING)
    county = models.ForeignKey(County, help_text='Powiat', on_delete=models.DO_NOTHING)
    place = models.CharField(max_length=32, help_text='Miejscowość')
    postal_code = models.CharField(max_length=16, help_text='Kod pocztowy')
    postal_place = models.CharField(max_length=32, help_text='Poczta')
    address = models.CharField(max_length=32, help_text='Adres, ulica i numer')

    # lokalizacja
    geo_lat = models.FloatField(blank=True)
    geo_lng = models.FloatField(blank=True)

    # podzial administracyjny koscielny
    diocese = models.ForeignKey(Diocese, on_delete=models.DO_NOTHING)
    deanery = models.ForeignKey(Deanery, null=True, on_delete=models.DO_NOTHING)

    # podzial ziem I RP.
    ziemia_i_rp = models.ForeignKey(ZiemiaIRP, null=True, on_delete=models.DO_NOTHING, help_text='Ziemia I RP')

    # kontakt
    phone = models.CharField(max_length=32, help_text=16, blank=True)
    link = models.URLField(blank=True)

    gen_id = models.IntegerField(default=0, unique=True)

    def __str__(self):
        return u'%d. %s' % (self.id, self.name)

    class Meta:
        verbose_name_plural = "parishes"


class ParishRawData(models.Model):
    parish = models.ForeignKey(Parish, on_delete=models.DO_NOTHING)
    data_key = models.CharField(max_length=16)
    data = models.TextField(blank=True)


class ParishUser(models.Model):
    parish = models.ForeignKey(Parish, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    note = models.TextField(blank=True)


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


class ParishRef(models.Model):
    parish = models.ForeignKey(Parish, on_delete=models.DO_NOTHING)
    documents_group = models.ForeignKey('DocumentGroup', on_delete=models.DO_NOTHING)
    key = models.TextField(blank=True)

    def __unicode__(self):
        return u'%s' % self.name


DOCUMENT_GROUP_TYPE = (
    (0, 'Documents'),   # fizyczne dokumenty
    (1, 'Photos'),      # zdjecia cyfrowe
    (2, 'Indexes'),     # indexy
)


class DocumentSource(models.Model):
    """
    0. familysearch.org
    1. geneteka.genealodzy.pl
    2. metryki.genealodzy
    3. szukajwarchiwach.pl
    4. metryki.genbaza.pl
    5. poznan-project.psnc.pl
    6. basia.famula.pl
    7. lubgens.eu

    8. księgi metrykalne analogowe
    """

    name = models.CharField(max_length=32)
    url = models.URLField(max_length=64, blank=True)

    def __str__(self):
        return u'%s' % (self.name)


class DocumentGroup(models.Model):
    name = models.CharField(max_length=32, help_text='Nazwa grupy dokumentów')
    url = models.URLField(blank=True, help_text='Adres url pod którym dokumenty są dostępne')

    parish = models.ForeignKey(Parish, on_delete=models.DO_NOTHING, help_text='Parafia')
    #parish_ref = models.ForeignKey(ParishRef, null=True, on_delete=models.DO_NOTHING)
    source = models.ForeignKey(DocumentSource, on_delete=models.DO_NOTHING)

    type = models.IntegerField(choices=DOCUMENT_GROUP_TYPE, help_text='Typ dokumentów')
    type_b = models.BooleanField(default=False, help_text='Akty urodzenia')
    type_d = models.BooleanField(default=False, help_text='Akty zgonu')
    type_m = models.BooleanField(default=False, help_text='Akty małżeństwa')
    type_a = models.BooleanField(default=False, help_text='Alegaty')

    date_from = models.IntegerField(help_text='Zakres dat: od roku', default=1800)
    date_to = models.IntegerField(help_text='Zakres dat: do roku', default=1900)
    date_excepts = models.TextField(blank=True, help_text='Lata pominięte')

    note = models.TextField(blank=True, help_text='Notatka')

    date_created = models.DateTimeField(blank=True, null=True, help_text='Data utworzenia')
    date_modified = models.DateTimeField(blank=True, null=True, help_text='Data utworzenia')
    user = models.ForeignKey(User, null=True, help_text='Autor rekordu', on_delete=models.DO_NOTHING)

