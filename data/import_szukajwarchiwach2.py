#!/bin/env python3

from splinter import Browser
from filecache import filecache
from pyquery import PyQuery

@filecache(30 * 24 * 60 * 60)
def get_collection(collection_id):
    url = 'https://www.szukajwarchiwach.gov.pl/zespol/-/zespol/{}'.format(collection_id)
    print(url)

    collections = []
    browser = Browser('chrome', headless=True)
    browser.visit(url)

    # wybieramy liste jednostek i ustawiam 200 per page
    link = browser.find_by_id('przejdzDoJednostek')
    if link.is_empty():
        print('brak jednostek; return')
        return collections

    link.click()
    if not browser.find_by_css('.dropdown.pagination-items-per-page').is_empty():
        browser.find_by_css('.dropdown.pagination-items-per-page')[0].click()
        browser.find_by_text('200')[0].click()

    # w petli pobieram kolejne strony
    while True:
        last_link = None
        if not browser.find_by_css('.pagination').is_empty():
            last_link = browser.find_by_css('.pagination')[0].find_by_tag('a').last

        # pobieramy tabelke
        collections.append(browser.find_by_css('.jednostkaObiekty')[0].html)
        """
        for tr in browser.find_by_css('.jednostkaObiekty')[0].find_by_tag('tr'):
            tds = tr.find_by_tag('td')

            # jesli to jest naglowej gdzie nie ma td to nara
            if len(tds) == 0:
                continue

            sygnatura = tds[0].text
            nazwa = tds[1].text
            daty = tds[2].text
            skany = tds[3].text
            href = tds[1].find_by_tag('a')._element.get_attribute('href')

            collections.append([sygnatura, nazwa, daty, skany, href])
        """

        # jesli jest nastepna strona to lecimy dalej
        if last_link is None or ('javascript:;' == last_link._element.get_attribute('href')):
            break
        print('next page')
        last_link.click()

    return collections


@filecache(30 * 24 * 60 * 60)
def get_archive(slug):
    """
    Zwraca zespoly z archiwum

    :param slug:
    :param page: int|None, None oznacza pobranie wszystkich stron
    :return:
    """

    url = 'https://www.szukajwarchiwach.gov.pl{}'.format(slug)
    zespoly = []

    browser = Browser('chrome', headless=True)
    browser.visit(url)
    print(url)

    # wybieramy liste zespolow i ustawiam 200 per page
    browser.find_by_text('Lista zespołów')[0].click()
    browser.find_by_css('.dropdown.pagination-items-per-page')[0].click()
    browser.find_by_text('200')[0].click()

    # w petli pobieram kolejne strony
    while True:
        last_link = browser.find_by_css('.pagination')[0].find_by_tag('a').last

        # pobieramy tabelke
        for tr in browser.find_by_css('.lista-zespolow-wyniki')[0].find_by_tag('tr'):

            if tr._element.get_attribute('class') == 'entityDetails':
                continue
            tds = tr.find_by_tag('td')
            if len(tds) == 0:
                continue
            sygnatura = tds[0].text
            nazwa = tds[1].text
            daty = tds[2].text
            skany = tds[3].text

            href = tds[1].find_by_tag('a')._element.get_attribute('href')
            zespol_id = href.split('/').pop()

            collections = get_collection(zespol_id)

            zespoly.append([sygnatura, nazwa, daty, skany, href, zespol_id, collections])

        # jesli jest nastepna strona to lecimy dalej
        if 'javascript:;' == last_link._element.get_attribute('href'):
            break
        print('next page')
        last_link.click()

    return zespoly


def parse_collection_html(data):
    rows = []
    html = PyQuery(data)
    for tr in html('tr'):
        tds = tr.findall('td')
        if len(tds) == 4:
            sygnatura = tds[0].findtext('a')
            nazwa = tds[1].findtext('a')
            daty = tds[2].findtext('a')
            skany = tds[3].findtext('a')
            rows.append([sygnatura, nazwa, daty, skany])
    return rows


def right_name(nazwa):
    ELEM = ['Akta stanu cywilnego', 'Akta kościelne', 'Parafia ', 'Sobór', 'Cerkiew', 'Akta kościelne']
    for EL in ELEM:
        if nazwa.lower().find(EL.lower()) > -1:
            return True
    return False


zespoly = get_archive('/web/archiwum-panstwowe-w-bialymstoku')
for z in zespoly:

    nazwa = z[1]
    if not right_name(nazwa):
        continue

    print('zespol; "{}"; "{}"; "{}"; "{}"; {};'.format(z[0].replace('"', ""), z[1], z[2], z[3], z[4], z[5]))
    rows = []
    for c in z[6]:
        rows.extend(parse_collection_html(c))
    for row in rows:
        print('kolekcja; "{}"; "{}"; "{}"; "{}"'.format(row[0], row[1], row[2], row[3]))


import os, sys
sys.exit(0)


ARCHIWA = [
    '/web/archiwum-akt-dawnych-diecezji-torunskiej',
    '/web/archiwum-akt-nowych',
    '/web/archiwum-biblioteki-polskiej-im.-ignacego-domeyki',
    '/web/archiwum-fundacji-kultury-i-dziedzictwa-ormian-polskich',
    '/web/archiwum-glowne-akt-dawnych',
    '/web/archiwum-instytutu-hoovera',
    '/web/archiwum-komisji-krajowej-nszz-solidarnosc',
    '/web/archiwum-muzeum-narodowego-w-krakowie',
    '/web/archiwum-muzeum-zamoyskich-w-kozlowce',
    '/web/archiwum-narodowe-w-krakowie',
    '/web/archiwum-narodowe-w-krakowie-oddzial-w-bochni',
    '/web/archiwum-narodowe-w-krakowie-oddzial-w-nowym-saczu',
    '/web/archiwum-narodowe-w-krakowie-oddzial-w-tarnowie',
    '/web/archiwum-nauki-polskiej-akademii-nauk-i-polskiej-akademii-umiejetnosci',
    '/web/archiwum-panstwowe-w-bialymstoku',
    '/web/archiwum-panstwowe-w-bialymstoku-oddzial-w-lomzy',
    '/web/archiwum-panstwowe-w-bydgoszczy',
    '/web/archiwum-panstwowe-w-bydgoszczy-oddzial-w-inowroclawiu',
    '/web/archiwum-panstwowe-w-czestochowie',
    '/web/archiwum-panstwowe-we-wroclawiu',
    '/web/archiwum-panstwowe-we-wroclawiu-oddzial-w-boleslawcu',
    '/web/archiwum-panstwowe-we-wroclawiu-oddzial-w-jeleniej-gorze',
    '/web/archiwum-panstwowe-we-wroclawiu-oddzial-w-kamiencu-zabkowickim',
    '/web/archiwum-panstwowe-we-wroclawiu-oddzial-w-legnicy',
    '/web/archiwum-panstwowe-w-gdansku',
    '/web/archiwum-panstwowe-w-gdansku-oddzial-w-gdyni',
    '/web/archiwum-panstwowe-w-gorzowie-wielkopolskim',
    '/web/archiwum-panstwowe-w-kaliszu',
    '/web/archiwum-panstwowe-w-katowicach',
    '/web/archiwum-panstwowe-w-katowicach-oddzial-w-bielsku-bialej',
    '/web/archiwum-panstwowe-w-katowicach-oddzial-w-cieszynie',
    '/web/archiwum-panstwowe-w-katowicach-oddzial-w-gliwicach',
    '/web/archiwum-panstwowe-w-katowicach-oddzial-w-pszczynie',
    '/web/archiwum-panstwowe-w-katowicach-oddzial-w-raciborzu',
    '/web/archiwum-panstwowe-w-kielcach',
    '/web/archiwum-panstwowe-w-kielcach-oddzial-w-sandomierzu',
    '/web/archiwum-panstwowe-w-koszalinie',
    '/web/archiwum-panstwowe-w-koszalinie-oddzial-w-slupsku',
    '/web/archiwum-panstwowe-w-koszalinie-oddzial-w-szczecinku',
    '/web/archiwum-panstwowe-w-lesznie',
    '/web/archiwum-panstwowe-w-lublinie',
    '/web/archiwum-panstwowe-w-lublinie.-oddzial-w-chelmie',
    '/web/archiwum-panstwowe-w-lublinie.-oddzial-w-krasniku',
    '/web/archiwum-panstwowe-w-lublinie.-oddzial-w-radzyniu-podlaskim',
    '/web/archiwum-panstwowe-w-lodzi',
    '/web/archiwum-panstwowe-w-lodzi-oddzial-w-sieradzu',
    '/web/archiwum-panstwowe-w-malborku',
    '/web/archiwum-panstwowe-w-olsztynie',
    '/web/archiwum-panstwowe-w-opolu',
    '/web/archiwum-panstwowe-w-piotrkowie-trybunalskim',
    '/web/archiwum-panstwowe-w-piotrkowie-trybunalskim-oddzial-w-tomaszowie-mazowieckim',
    '/web/archiwum-panstwowe-w-plocku',
    '/web/archiwum-panstwowe-w-plocku-oddzial-w-kutnie',
    '/web/archiwum-panstwowe-w-plocku-oddzial-w-eczycy',
    '/web/archiwum-panstwowe-w-poznaniu',
    '/web/archiwum-panstwowe-w-poznaniu-oddzial-w-gnieznie',
    '/web/archiwum-panstwowe-w-poznaniu-oddzial-w-koninie',
    '/web/archiwum-panstwowe-w-poznaniu-oddzial-w-pile',
    '/web/archiwum-panstwowe-w-przemyslu',
    '/web/archiwum-panstwowe-w-radomiu',
    '/web/archiwum-panstwowe-w-rzeszowie',
    '/web/archiwum-panstwowe-w-rzeszowie-oddzial-w-sanoku',
    '/web/archiwum-panstwowe-w-siedlcach',
    '/web/archiwum-panstwowe-w-suwalkach',
    '/web/archiwum-panstwowe-w-suwalkach-oddzial-w-elku',
    '/web/archiwum-panstwowe-w-szczecinie',
    '/web/archiwum-panstwowe-w-szczecinie-oddzial-w-miedzyzdrojach',
    '/web/archiwum-panstwowe-w-szczecinie-oddzial-w-stargardzie',
    '/web/archiwum-panstwowe-w-toruniu',
    '/web/archiwum-panstwowe-w-toruniu-oddzial-we-wloclawku',
    '/web/archiwum-panstwowe-w-warszawie',
    '/web/archiwum-panstwowe-w-warszawie-oddzial-w-grodzisku-mazowieckim',
    '/web/archiwum-panstwowe-w-warszawie-oddzial-w-lowiczu',
    '/web/archiwum-panstwowe-w-warszawie-oddzial-w-mlawie',
    '/web/archiwum-panstwowe-w-warszawie-oddzial-w-otwocku',
    '/web/archiwum-panstwowe-w-warszawie-oddzial-w-pultusku',
    '/web/archiwum-panstwowe-w-zamosciu',
    '/web/archiwum-panstwowe-w-zielonej-gorze',
    '/web/archiwum-politechniki-krakowskiej-im.-tadeusza-kosciuszki',
    '/web/archiwum-polskiej-akademii-nauk-w-warszawie',
    '/web/archiwum-polskiej-misji-katolickiej-we-francji',
    '/web/archiwum-polskiej-misji-katolickiej-w-szwajcarii',
    '/web/archiwum-polskiej-prowincji-dominikanow',
    '/web/archiwum-uniwersytetu-jagiellonskiego',
    '/web/archiwum-uniwersytetu-rolniczego-im.-hugona-kollataja-w-krakowie',
    '/web/archiwum-uniwersytetu-szczecinskiego',
    '/web/archiwum-zgromadzenia-zmartwychwstania-panskiego-w-rzymie',
    '/web/centralne-archiwum-polonii-w-orchard-lake',
    '/web/centralne-muzeum-jencow-wojennych',
    '/web/fundacja-archeologia-fotografii',
    '/web/fundacja-archivum-helveto-polonicum',
    '/web/fundacja-im.-zofii-i-jana-wlodkow',
    '/web/fundacja-sztuki-wspolczesnej-in-situ',
    '/web/instytut-im.-jerzego-grotowskiego',
    '/web/klasztor-siostr-karmelitanek-bosych-w-krakowie',
    '/web/klub-inteligencji-katolickiej',
    '/web/muzeum-romantyzmu-w-opinogorze',
    '/web/muzeum-uniwersytetu-opolskiego',
    '/web/narodowe-archiwum-cyfrowe',
    '/web/papieski-instytut-studiow-koscielnych-w-rzymie',
    '/web/polish-music-center',
    '/web/polska-akademia-nauk-archiwum-w-warszawie-oddzial-w-katowicach',
    '/web/polska-akademia-nauk-archiwum-w-warszawie-oddzial-w-poznaniu',
    '/web/polski-instytut-badawczy-i-muzeum-w-budapeszcie',
    '/web/polski-instytut-naukowy-w-ameryce',
    '/web/uniwersytet-jana-kochanowskiego-w-kielcach',
    '/web/zwiazek-sybirakow-zarzad-glowny',
]


def get_unit():
    pass





for ARCH in ARCHIWA:
    print(get_archive(ARCH))
    break

"""
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 17 18 21 24 26  27 28 29 30 31 32 33 34 35 36 37 38 39 41 42 45 48 49 50 \
    51 52 53 54 55 56 58 59 60 62 63 64 65 66 67 68 69 71 72 73 75 76 78 79 82 83 84 85 86 88 89 92 93; do

    if [[ "$i" != "4" ]] && [[ "$i" != "5" ]]; then
        continue
    fi

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
	    if [[ "`echo "$TITLE" | grep "akta stanu cywilnego"`" != "" ]] || [[ "`echo "$TITLE" | grep "Parafii "`" != "" ]] || [[ "`echo "$TITLE" | grep "Parafia "`" != "" ]]; then
	            echo "$NUMBER; $TITLE; $YEARS; $PHOTOS";
		fi
        done
    done
done

# todo ./import_szukajwarchiwach.sh | grep Parafi
"""