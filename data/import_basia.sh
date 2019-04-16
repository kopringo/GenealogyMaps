#!/bin/bash

# http://www.basia.famula.pl/pl/skany
# uniq key:
# - placeid
#
# search:
# - powiat + miejsowosc
# - wspolrzedne geo.
#
# Decyzja:
# - najpierw zaladowac szukajwarchiwach. te dane tutaj wskazują stan indeksacji. maja mniejsze znaczenie.
#

FORCE=0

if [[ ! -f cache/basia_root ]] || [[ "$FORCE" == "1" ]]; then
    wget "http://www.basia.famula.pl/pl/skany" -O cache/basia_root;
fi

grep "skany.php?placeid" cache/basia_root | grep -v facebook | sed -e 's/.*placeid=//g' | sed -e "s/'.*//g" | sort | uniq | sort -n > cache/basia_root_placeids
for id in `cat cache/basia_root_placeids`; do
    #echo $id;
    position=`grep " pos$id = " cache/basia_root | sed -e 's/.*LatLng.//g' | sed -e "s/).*//g" | head -n1`
    name=`grep "id='anchor$id'" cache/basia_root | sed -e 's/.*anchor//g' | sed -e 's/<.*//g' | sed -e 's/.*>//g'`
    echo "$id: [$position] $name";
done

# todo final format