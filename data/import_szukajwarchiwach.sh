#!/bin/bash

# view-source:http://mapy.lubgens.eu/
# uniq key:
# - numer zespołu
#
# search:
# - recznie...

# https://szukajwarchiwach.pl/4/str/1/100?sort=tytul#tabZasoby

#<li><a href="/1">Archiwum Główne Akt Dawnych</a></li>
#<li><a href="/2">Archiwum Akt Nowych</a></li>
#<li><a href="/3">Narodowe Archiwum Cyfrowe</a></li>
#<li><a href="/4">Archiwum Państwowe w Białymstoku</a></li>
#<li><a href="/5">Archiwum Państwowe w Białymstoku Oddział w Łomży</a></li>
#<li><a href="/6">Archiwum Państwowe w Bydgoszczy</a></li>
#<li><a href="/7">Archiwum Państwowe w Bydgoszczy Oddział w Inowrocławiu</a></li>
#<li><a href="/8">Archiwum Państwowe w Częstochowie</a></li>
#<li><a href="/9">Archiwum Państwowe w Malborku</a></li>
#<li><a href="/10">Archiwum Państwowe w Gdańsku</a></li>
#<li><a href="/11">Archiwum Państwowe w Kaliszu</a></li>
#<li><a href="/12">Archiwum Państwowe w Katowicach</a></li>
#<li><a href="/13">Archiwum Państwowe w Katowicach Oddział w Bielsku-Białej</a></li>
#<li><a href="/14">Archiwum Państwowe w Katowicach Oddział w Cieszynie</a></li>
#<li><a href="/15">Archiwum Państwowe w Katowicach Oddział w Gliwicach</a></li>
#<li><a href="/17">Archiwum Państwowe w Katowicach Oddział w Pszczynie</a></li>
#<li><a href="/18">Archiwum Państwowe w Katowicach Oddział w Raciborzu</a></li>
#<li><a href="/21">Archiwum Państwowe w Kielcach</a></li>
#<li><a href="/24">Archiwum Państwowe w Kielcach Oddział w Sandomierzu</a></li>
#<li><a href="/26">Archiwum Państwowe w Koszalinie</a></li>
#<li><a href="/27">Archiwum Państwowe w Koszalinie Oddział w Słupsku</a></li>
#<li><a href="/28">Archiwum Państwowe w Koszalinie Oddział w Szczecinku</a></li>
#<li><a href="/29">Archiwum Narodowe w Krakowie</a></li>
#<li><a href="/30">Archiwum Narodowe w Krakowie Oddział w Bochni</a></li>
#<li><a href="/31">Archiwum Narodowe w Krakowie Oddział w Nowym Sączu</a></li>
#<li><a href="/33">Archiwum Narodowe w Krakowie Oddział w Tarnowie</a></li>
#<li><a href="/34">Archiwum Państwowe w Lesznie</a></li>
#<li><a href="/35">Archiwum Państwowe w Lublinie</a></li>
#<li><a href="/36">Archiwum Państwowe w Lublinie Oddział w Chełmie</a></li>
#<li><a href="/37">Archiwum Państwowe w Lublinie Oddział w Kraśniku</a></li>
#<li><a href="/38">Archiwum Państwowe w Lublinie Oddział w Radzyniu Podlaskim</a></li>
#<li><a href="/39">Archiwum Państwowe w Łodzi</a></li>
#<li><a href="/41">Archiwum Państwowe w Łodzi Oddział w Sieradzu</a></li>
#<li><a href="/42">Archiwum Państwowe w Olsztynie</a></li>
#<li><a href="/45">Archiwum Państwowe w Opolu</a></li>
#<li><a href="/48">Archiwum Państwowe w Piotrkowie Trybunalskim</a></li>
#<li><a href="/49">Archiwum Państwowe w Piotrkowie Trybunalskim Oddział w Tomaszowie Mazowieckim</a></li>
#<li><a href="/50">Archiwum Państwowe w Płocku</a></li>
#<li><a href="/51">Archiwum Państwowe w Płocku Oddział w Kutnie</a></li>
#<li><a href="/52">Archiwum Państwowe w Płocku Oddział w Łęczycy</a></li>
#<li><a href="/53">Archiwum Państwowe w Poznaniu</a></li>
#<li><a href="/54">Archiwum Państwowe w Poznaniu Oddział w Koninie</a></li>
#<li><a href="/55">Archiwum Państwowe w Poznaniu Oddział w Pile</a></li>
#<li><a href="/56">Archiwum Państwowe w Przemyślu</a></li>
#<li><a href="/58">Archiwum Państwowe w Radomiu</a></li>
#<li><a href="/59">Archiwum Państwowe w Rzeszowie</a></li>
#<li><a href="/60">Archiwum Państwowe w Rzeszowie Oddział w Sanoku</a></li>
#<li><a href="/62">Archiwum Państwowe w Siedlcach</a></li>
#<li><a href="/63">Archiwum Państwowe w Suwałkach</a></li>
#<li><a href="/64">Archiwum Państwowe w Suwałkach Oddział w Ełku</a></li>
#<li><a href="/65">Archiwum Państwowe w Szczecinie</a></li>
#<li><a href="/66">Archiwum Państwowe w Gorzowie Wielkopolskim</a></li>
#<li><a href="/67">Archiwum Państwowe w Szczecinie Oddział w Międzyzdrojach</a></li>
#<li><a href="/68">Archiwum Państwowe w Szczecinie Oddział w Stargardzie</a></li>
#<li><a href="/69">Archiwum Państwowe w Toruniu</a></li>
#<li><a href="/71">Archiwum Państwowe w Toruniu Oddział we Włocławku</a></li>
#<li><a href="/72">Archiwum Państwowe w Warszawie</a></li>
#<li><a href="/73">Archiwum Państwowe w Warszawie Oddział w Grodzisku Mazowieckim</a></li>
#<li><a href="/75">Archiwum Państwowe w Warszawie Oddział w Łowiczu</a></li>
#<li><a href="/76">Archiwum Państwowe w Warszawie Oddział w Mławie</a></li>
#<li><a href="/78">Archiwum Państwowe w Warszawie Oddział w Otwocku</a></li>
#<li><a href="/79">Archiwum Państwowe w Warszawie Oddział w Pułtusku</a></li>
#<li><a href="/82">Archiwum Państwowe we Wrocławiu</a></li>
#<li><a href="/83">Archiwum Państwowe we Wrocławiu Oddział w Jeleniej Górze</a></li>
#<li><a href="/84">Archiwum Państwowe we Wrocławiu Oddział w Kamieńcu Ząbkowickim</a></li>
#<li><a href="/85">Archiwum Państwowe we Wrocławiu Oddział w Legnicy</a></li>
#<li><a href="/86">Archiwum Państwowe we Wrocławiu Oddział w Bolesławcu</a></li>
#<li><a href="/88">Archiwum Państwowe w Zamościu</a></li>
#<li><a href="/89">Archiwum Państwowe w Zielonej Górze</a></li>
#<li><a href="/92">Archiwum Państwowe w Poznaniu Oddział w Gnieźnie</a></li>
#<li><a href="/93">Archiwum Państwowe w Gdańsku Oddział w Gdyni</a></li>
#<li><a href="/302">Archiwum Polskiej Akademii Nauk w Warszawie</a></li>
#<li><a href="/345">Archiwum Fundacji Kultury i Dziedzictwa Ormian Polskich</a></li>
#<li><a href="/346">Centralne Muzeum Jeńców Wojennych w Łambinowicach-Opolu</a></li>
#<li><a href="/365">Muzeum Romantyzmu w Opinogórze</a></li>
#<li><a href="/705">Papieski Instytut Studiów Kościelnych w Rzymie</a></li>
#<li><a href="/707">Archiwum Polskiej Misji Katolickiej w Szwajcarii</a></li>
#<li><a href="/708">Centralne Archiwum Polonii w Orchard Lake</a></li>
#<li><a href="/713">Archiwum Biblioteki Polskiej im. Ignacego Domeyki</a></li>
#<li><a href="/800">Archiwum Instytutu Hoovera</a></li>
#<li><a href="/802">Archiwum Muzeum Narodowego w Krakowie</a></li>
#<li><a href="/804">Archiwum Muzeum Zamoyskich w Kozłówce</a></li>

for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 17 18 21 24 26  27 28 29 30 31 32 33 34 35 36 37 38 39 41 42 45 48 49 50 \
    51 52 53 54 55 56 58 59 60 62 63 64 65 66 67 68 69 71 72 73 75 76 78 79 82 83 84 85 86 88 89 92 93; do

    if [[ ! -f cache/szwa_zasob_$i ]]; then
        wget "https://szukajwarchiwach.pl/$i/str/1/100?sort=tytul" --no-check-certificate -q -O cache/szwa_zasob_$i;
    fi
    MAX_ID=`cat cache/szwa_zasob_$i | grep "=tytul#tabZasoby" | tail -n 1 | sed -e 's/.*Zasoby..//g' | sed -e 's/<.*//g'`
    echo "$i MAX_ID $MAX_ID";
    for page in `seq 1 $MAX_ID`; do
        if [[ ! -f cache/szwa_zasob_$i"_"$page ]]; then
            wget "https://szukajwarchiwach.pl/$i/str/$page/100?sort=tytul" --no-check-certificate -q -O cache/szwa_zasob_$i"_"$page;
        fi

        LINES=`grep -n "<tr class=" cache/szwa_zasob_$i"_"$page | awk '{print $1}' | sed -e 's/://g'`;
        for LINE in $LINES; do
            cat cache/szwa_zasob_$i"_"$page | tail -n +$LINE | head -n 6 > cache/szwa_zasob_single;
            cat cache/szwa_zasob_single | sed -e "s/<\/a><\/td>//g" | sed -e "s/<\/span><\/td>//g" | sed -e "s/.*>//g" > cache/szwa_zasob_single2;
            NUMBER=`cat cache/szwa_zasob_single2 | head -n 2 | tail -n 1`
            TITLE=`cat cache/szwa_zasob_single2 | head -n 3 | tail -n 1`
            YEARS=`cat cache/szwa_zasob_single2 | head -n 4 | tail -n 1`
            PHOTOS=`cat cache/szwa_zasob_single2 | head -n 5 | tail -n 1`
            echo "$NUMBER; $TITLE; $YEARS; $PHOTOS";
        done
    done
done