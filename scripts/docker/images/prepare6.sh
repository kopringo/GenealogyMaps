#!/bin/bash

set -e

export LC_ALL=C
export DEBIAN_FRONTEND=noninteractive
minimal_apt_get_install='apt-get install -y '

apt-get update
$minimal_apt_get_install apt-transport-https ca-certificates apt-utils wget curl git runit zip unzip make net-tools vim;

$minimal_apt_get_install php7.2-dev php7.2-fpm php7.2-mysql php7.2-curl php7.2-zip php7.2-json php7.2-gmp php7.2-xml php7.2-soap php7.2-apcu php7.2-mbstring php-sqlite3 php-pear php7.2-redis;
$minimal_apt_get_install python3.7 python3-pip uwsgi uwsgi-plugin-python3;
$minimal_apt_get_install gcc g++ mysql-client;

curl -sL https://deb.nodesource.com/setup_10.x | bash -;
apt-get install -y nodejs;

wget https://getcomposer.org/composer.phar -O /usr/bin/composer;
chmod +x /usr/bin/composer

wget http://www.phing.info/get/phing-latest.phar
chmod +x phing-latest.phar
mv phing-latest.phar /usr/bin/phing

# php7
cp /bd_build/image/fpm-www.conf /etc/php/7.2/fpm/pool.d/www.conf
mkdir -p /var/run/php/

# python
cp /bd_build/image/uwsgi.ini /etc/uwsgi/apps-enabled/app.ini

cp /bd_build/image/run_uwsgi /bin/;
cp /bd_build/image/run_fpm /bin/;
cp /bd_build/image/run_empty /bin/;
cp /bd_build/image/run_console /bin/;

if [[ -f /usr/bin/nodejs ]] && [[ ! -f /usr/bin/node ]]; then
        ln -s /usr/bin/nodejs /usr/bin/node;
fi

echo "[done]";
