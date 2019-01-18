#!/bin/bash

# view-source:http://mapy.lubgens.eu/
# uniq key:
# - nazwa miejscowosci + wsp. uproszczone.
#
# search:
# - wspolrzedne geo.

FORCE=0

if [[ ! -f cache/lubgens_root ]] || [[ "$FORCE" == "1" ]]; then
    wget "https://mapy.lubgens.eu/" -O cache/lubgens_root --header "User-Agent: Mozilla/5.0";
fi

for i in `grep "var R" cache/lubgens_root -n | awk '{print $1}' | sed -e 's/://g'`; do
    cat cache/lubgens_root | tail -n +$i | head -n 11 > cache/lubgens_single;
    cat cache/lubgens_single;
    echo "===============================";


done