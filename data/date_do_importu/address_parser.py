#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pyexcel_ods, os, sys, codecs

filepath = sys.argv[1]
book = pyexcel_ods.get_data(filepath)
sheets = book

sheet = sheets['Arkusz1']

postal_index = None
geo_lat_index = None
geo_lng_index = None
miejscowosc_index = None

index = 0
for field in sheet[0]:
    if field in ('postal_apcode', 'postal_code'):
        postal_index = index
    if field in ('geo_lat'):
        geo_lat_index = index
    if field in ('geo_lng'):
        geo_lng_index = index
    if field in ('miejscowosc'):
        miejscowosc_index = index

    index = index + 1

print(postal_index, geo_lat_index, geo_lng_index, miejscowosc_index)

for row in sheet[1:]:
    print('%s:%s:%s:%s' % (row[miejscowosc_index].strip(), str(row[geo_lat_index]).strip(), str(row[geo_lng_index]).strip(), row[postal_index]))