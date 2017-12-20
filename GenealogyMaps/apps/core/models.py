from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Source(models.Model):
    name = models.CharField(max_length=32)
    url = models.URLField(blank=True)

    def __unicode__(self):
        return u'%s' % self.name


class Parish(models.Model):
    name = models.CharField(max_length=32)
    year = models.IntegerField(blank=True)
    address = models.CharField(max_length=32)
    geo_lat = models.FloatField(blank=True)
    geo_lon = models.FloatField(blank=True)
    link = models.URLField(blank=True)
    phone = models.CharField(max_length=16, blank=True)

    def __unicode__(self):
        return u'%s' % self.name


class ParishUser(models.Model):
    parish = models.ForeignKey(Parish, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    note = models.TextField(blank=True)


class ParishRef(models.Model):
    parish = models.ForeignKey(Parish, on_delete=models.DO_NOTHING)
    source = models.ForeignKey(Source, on_delete=models.DO_NOTHING)
    key = models.TextField(blank=True)

    def __unicode__(self):
        return u'%s' % self.name


DOCUMENT_GROUP_TYPE = (
    (1, 'Photos'),
    (2, 'Indexes'),
)


class DocumentGroup(models.Model):
    parish = models.ForeignKey(Parish, on_delete=models.DO_NOTHING)
    parish_ref = models.ForeignKey(ParishRef, null=True, on_delete=models.DO_NOTHING)
    type = models.IntegerField(choices=DOCUMENT_GROUP_TYPE)
    type_b = models.BooleanField()
    type_d = models.BooleanField()
    type_m = models.BooleanField()
    type_a = models.BooleanField()
    date_from = models.DateField()
    date_to = models.DateField()
    note = models.TextField(blank=True)
