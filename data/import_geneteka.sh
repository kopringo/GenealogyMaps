#! /bin/bash

# https://geneteka.genealodzy.pl/rejestry.php?lang=pol
# uniq key:
# - id parafii
#
# search:
# - wojewodztwo + miejsowosc (opcjonalnie powiat czasem jest dost).

FORCE=0

if [[ ! -f cache/geneteka_root ]] || [[ "$FORCE" == "1" ]]; then
    wget "https://geneteka.genealodzy.pl/rejestry.php?lang=pol" -O cache/geneteka_root;
fi

# geneteka_root_details
cat cache/geneteka_root | sed -e 's/<\/font>/\n/g' | grep "index.php?rid" | sed -e 's/index.php.rid=/ /g' | sed -e 's/&amp;/ /g' | sed -e 's/title=.//g' | sed -e 's/">/ | /g' | sed -e 's/<\/a.*//g'

# todo pobrac dane z /index.php?rid=3328&w=02kp&op=gt
# i znalezc link do http://parafie.genealodzy.pl/index.php?op=pr&pid=6286