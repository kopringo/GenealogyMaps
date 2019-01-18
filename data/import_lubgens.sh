#!/bin/bash

# view-source:http://mapy.lubgens.eu/

FORCE=0

if [[ ! -f cache/lubgens_root ]] || [[ "$FORCE" == "1" ]]; then
    wget "http://mapy.lubgens.eu/" -O cache/lubgens_root;
fi