<?php



$wojewodztwa_by_name = array();
$wojewodztwa = array(
    1 => array('id' => 1, 'short' => 'DS','name' => 'dolnośląskie', 'visible' => true),
    2 => array('id' => 2, 'short' => 'KP','name' => 'kujawsko-pomorskie', 'visible' => true),
    3 => array('id' => 3, 'short' => 'LB','name' => 'lubelskie', 'visible' => true),
    4 => array('id' => 4, 'short' => 'LS','name' => 'lubuskie', 'visible' => true),
    5 => array('id' => 5, 'short' => 'LD','name' => 'łódzkie', 'visible' => true),
    6 => array('id' => 6, 'short' => 'MP','name' => 'małopolskie', 'visible' => true),
    7 => array('id' => 7, 'short' => 'MZ','name' => 'mazowieckie', 'visible' => true),
    8 => array('id' => 8, 'short' => 'OP','name' => 'opolskie', 'visible' => true),
    9 => array('id' => 9, 'short' => 'PK','name' => 'podkarpackie', 'visible' => true),
    10 => array('id' => 10, 'short' => 'PL','name' => 'podlaskie', 'visible' => true),
    11 => array('id' => 11, 'short' => 'PM','name' => 'pomorskie', 'visible' => true),
    12 => array('id' => 12, 'short' => 'SL','name' => 'śląskie', 'visible' => true),
    13 => array('id' => 13, 'short' => 'SK','name' => 'świętokrzyskie', 'visible' => true),
    14 => array('id' => 14, 'short' => 'WM','name' => 'warmińsko-mazurskie', 'visible' => true),
    15 => array('id' => 15, 'short' => 'WP','name' => 'wielkopolskie', 'visible' => true),
    16 => array('id' => 16, 'short' => 'ZP','name' => 'zachodniopomorskie', 'visible' => true),
    21 => array('id' => 21, 'short' => 'UK','name' => 'Ukraina', 'visible' => false),
    22 => array('id' => 22, 'short' => 'BI','name' => 'Białoruś', 'visible' => false),
    23 => array('id' => 23, 'short' => 'LI','name' => 'Litwa', 'visible' => false),
    155 => array('id' => 155, 'short' => '','name' => '', 'visible' => false),
    156 => array('id' => 156, 'short' => '','name' => '', 'visible' => false)
);
foreach($wojewodztwa as $wojewodztwo){
    $wojewodztwa_by_name[ strtolower($wojewodztwo['name']) ] = $wojewodztwo;
}

// https://pl.wikipedia.org/wiki/Dekanaty_Ko%C5%9Bcio%C5%82a_rzymskokatolickiego_w_Polsce
// + kompatybilnosc z genealodzy.pl
// ilosc dekanatow na 2017 rok
$diecezje = array(
    1 => array('id' => 1,'arch' => 'archi',     'short' => 'BIA','name' => 'białostocka','link' => 'http://pl.wikipedia.org/wiki/Archidiecezja_białostocka',        'dek_count' => 13, 'par_count' => 115),
    2 => array('id' => 2,'arch' => '',          'short' => 'BIE','name' => 'bielsko-żywiecka','link' => 'http://pl.wikipedia.org/wiki/Diecezja_bielsko-żywiecka',   'dek_count' => 22, 'par_count' => 210),
    3 => array('id' => 3,'arch' => '',          'short' => 'BYD','name' => 'bydgoska','link' => 'http://pl.wikipedia.org/wiki/Diecezja_bydgoska',                   'dek_count' => 19, 'par_count' => 150),
    4 => array('id' => 4,'arch' => 'archi',     'short' => 'CZE','name' => 'częstochowska','link' => 'http://pl.wikipedia.org/wiki/Archidiecezja_częstochowska',    'dek_count' => 35, 'par_count' => 311),
    5 => array('id' => 5,'arch' => '',          'short' => 'DRO','name' => 'drohiczyńska','link' => 'http://pl.wikipedia.org/wiki/Diecezja_drohiczyńska',           'dek_count' => 11, 'par_count' => 98),
    6 => array('id' => 6,'arch' => '',          'short' => 'ELB','name' => 'elbląska','link' => 'http://pl.wikipedia.org/wiki/Diecezja_elbląska',                   'dek_count' => 20, 'par_count' => 157),
    7 => array('id' => 7,'arch' => '',          'short' => 'ELC','name' => 'ełcka','link' => 'http://pl.wikipedia.org/wiki/Diecezja_ełcka',                         'dek_count' => 21, 'par_count' => 151),
    8 => array('id' => 8,'arch' => 'archi',     'short' => 'GDA','name' => 'gdańska','link' => 'http://pl.wikipedia.org/wiki/Archidiecezja_gdańska',                'dek_count' => 24, 'par_count' => 200),
    9 => array('id' => 9,'arch' => '',          'short' => 'GLI','name' => 'gliwicka','link' => 'http://pl.wikipedia.org/wiki/Diecezja_gliwicka',                   'dek_count' => 18, 'par_count' => 156),
    10 => array('id' => 10,'arch' => 'archi',   'short' => 'GNI','name' => 'gnieźnieńska','link' => 'http://pl.wikipedia.org/wiki/Archidiecezja_gnieźnieńska',      'dek_count' => 30, 'par_count' => 266),
    11 => array('id' => 11,'arch' => '',        'short' => 'KAL','name' => 'kaliska','link' => 'http://pl.wikipedia.org/wiki/Diecezja_kaliska',                     'dek_count' => 33, 'par_count' => 283),
    12 => array('id' => 12,'arch' => 'archi',   'short' => 'KAT','name' => 'katowicka','link' => 'http://pl.wikipedia.org/wiki/Archidiecezja_katowicka',            'dek_count' => 37, 'par_count' => 322),
    13 => array('id' => 13,'arch' => '',        'short' => 'KIE','name' => 'kielecka','link' => 'http://pl.wikipedia.org/wiki/Diecezja_kielecka',                   'dek_count' => 33, 'par_count' => 304),
    14 => array('id' => 14,'arch' => '',        'short' => 'KOS','name' => 'koszalińsko-kołobrzeska','link' => 'http://pl.wikipedia.org/wiki/Diecezja_koszalińsko-kołobrzeska', 'dek_count' => 24, 'par_count' => 221),
    15 => array('id' => 15,'arch' => 'archi',   'short' => 'KRA','name' => 'krakowska','link' => 'http://pl.wikipedia.org/wiki/Archidiecezja_krakowska',            'dek_count' => 45, 'par_count' => 448),
    16 => array('id' => 16,'arch' => '',        'short' => 'LEG','name' => 'legnicka','link' => 'http://pl.wikipedia.org/wiki/Diecezja_legnicka',                   'dek_count' => 28, 'par_count' => 238),
    17 => array('id' => 17,'arch' => 'archi',   'short' => 'LOD','name' => 'łódzka','link' => 'http://pl.wikipedia.org/wiki/Archidiecezja_łódzka',                  'dek_count' => 27, 'par_count' => 219),
    18 => array('id' => 18,'arch' => '',        'short' => 'LOM','name' => 'łomżyńska','link' => 'http://pl.wikipedia.org/wiki/Diecezja_łomżyńska',                 'dek_count' => 24, 'par_count' => 183),
    19 => array('id' => 19,'arch' => '',        'short' => 'LOW','name' => 'łowicka','link' => 'http://pl.wikipedia.org/wiki/Diecezja_łowicka',                     'dek_count' => 21, 'par_count' => 167),
    20 => array('id' => 20,'arch' => 'archi',   'short' => 'LUB','name' => 'lubelska','link' => 'http://pl.wikipedia.org/wiki/Archidiecezja_lubelska',              'dek_count' => 28, 'par_count' => 271),
    21 => array('id' => 21,'arch' => '',        'short' => 'OPO','name' => 'opolska','link' => 'http://pl.wikipedia.org/wiki/Diecezja_opolska',                     'dek_count' => 36, 'par_count' => 399),
    //
    23 => array('id' => 23,'arch' => '',        'short' => 'PEL','name' => 'pelplińska','link' => 'http://pl.wikipedia.org/wiki/Diecezja_pelplińska',               'dek_count' => 30, 'par_count' => 290),
    24 => array('id' => 24,'arch' => '',        'short' => 'PLO','name' => 'płocka','link' => 'http://pl.wikipedia.org/wiki/Diecezja_płocka',                       'dek_count' => 26, 'par_count' => 248),
    25 => array('id' => 25,'arch' => 'archi',   'short' => 'POZ','name' => 'poznańska','link' => 'http://pl.wikipedia.org/wiki/Archidiecezja_poznańska',            'dek_count' => 42, 'par_count' => 412),
    26 => array('id' => 26,'arch' => 'archi',   'short' => 'PRZ','name' => 'przemyska','link' => 'http://pl.wikipedia.org/wiki/Archidiecezja_przemyska',            'dek_count' => 41, 'par_count' => 398),
    27 => array('id' => 27,'arch' => '',        'short' => 'RAD','name' => 'radomska','link' => 'http://pl.wikipedia.org/wiki/Diecezja_radomska',                   'dek_count' => 29, 'par_count' => 304),
    28 => array('id' => 28,'arch' => '',        'short' => 'RZE','name' => 'rzeszowska','link' => 'http://pl.wikipedia.org/wiki/Diecezja_rzeszowska',               'dek_count' => 25, 'par_count' => 244),
    29 => array('id' => 29,'arch' => '',        'short' => 'SAN','name' => 'sandomierska','link' => 'http://pl.wikipedia.org/wiki/Diecezja_sandomierska',           'dek_count' => 24, 'par_count' => 243),
    30 => array('id' => 30,'arch' => '',        'short' => 'SIE','name' => 'siedlecka','link' => 'http://pl.wikipedia.org/wiki/Diecezja_siedlecka',                 'dek_count' => 25, 'par_count' => 247),
    31 => array('id' => 31,'arch' => '',        'short' => 'SOS','name' => 'sosnowiecka','link' => 'http://pl.wikipedia.org/wiki/Diecezja_sosnowiecka',             'dek_count' => 23, 'par_count' => 162),
    32 => array('id' => 32,'arch' => '',        'short' => 'SWI','name' => 'świdnicka','link' => 'http://pl.wikipedia.org/wiki/Diecezja_świdnicka',                 'dek_count' => 24, 'par_count' => 191),
    33 => array('id' => 33,'arch' => 'archi',   'short' => 'SZC','name' => 'szczecińsko-kamieńska','link' => 'http://pl.wikipedia.org/wiki/Archidiecezja_szczecińsko-kamieńska', 'dek_count' => 36, 'par_count' => 273),
    34 => array('id' => 34,'arch' => '',        'short' => 'TAR','name' => 'tarnowska','link' => 'http://pl.wikipedia.org/wiki/Diecezja_tarnowska',                 'dek_count' => 43, 'par_count' => 452),
    35 => array('id' => 35,'arch' => '',        'short' => 'TOR','name' => 'toruńska','link' => 'http://pl.wikipedia.org/wiki/Diecezja_toruńska',                   'dek_count' => 24, 'par_count' => 196),
    36 => array('id' => 36,'arch' => 'archi',   'short' => 'WAR','name' => 'warmińska','link' => 'http://pl.wikipedia.org/wiki/Archidiecezja_warmińska',            'dek_count' => 33, 'par_count' => 262),
    37 => array('id' => 37,'arch' => '',        'short' => 'WAS','name' => 'warszawsko-praska','link' => 'http://pl.wikipedia.org/wiki/Diecezja_warszawsko-praska', 'dek_count' => 20, 'par_count' => 184),
    38 => array('id' => 38,'arch' => 'archi',   'short' => 'WAW','name' => 'warszawska','link' => 'http://pl.wikipedia.org/wiki/Archidiecezja_warszawska',          'dek_count' => 28, 'par_count' => 213),
    39 => array('id' => 39,'arch' => '',        'short' => 'WLO','name' => 'włocławska','link' => 'http://pl.wikipedia.org/wiki/Diecezja_włocławska',               'dek_count' => 33, 'par_count' => 232),
    40 => array('id' => 40,'arch' => 'archi',   'short' => 'WRO','name' => 'wrocławska','link' => 'http://pl.wikipedia.org/wiki/Archidiecezja_wrocławska',          'dek_count' => 33, 'par_count' => 299),
    41 => array('id' => 41,'arch' => '',        'short' => 'ZAM','name' => 'zamojsko-lubaczowska','link' => 'http://pl.wikipedia.org/wiki/Diecezja_zamojsko-lubaczowska', 'dek_count' => 19, 'par_count' => 187),
    42 => array('id' => 42,'arch' => '',        'short' => 'ZIE','name' => 'zielonogórsko-gorzowska','link' => 'http://pl.wikipedia.org/wiki/Diecezja_zielonogórsko-gorzowska', 'dek_count' => 29, 'par_count' => 270),
    22 => array('id' => 22,'arch' => '',        'short' => 'ORD','name' => 'ordynariat polowy WP','link' => 'http://pl.wikipedia.org/wiki/Ordynariat_Polowy_Wojska_Polskiego',  'dek_count' => 9, 'par_count' => 80),
    44 => array('id' => 44,'arch' => '',        'short' => '','name' => 'nierozpoznana','link' => NULL, 'dek_count' => 0, 'par_count' => 0),
    0 => array('id' => 0,'arch' => '',          'short' => '0','name' => 'brak','link' => NULL, 'dek_count' => 0, 'par_count' => 0)
);
